from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower
from django.db.models import Avg

from reviews.models import Review
from reviews.forms import ReviewForm
from .models import Product, Category
from .forms import ProductForm

from profiles.models import UserProfile
from wishlist.models import WishList

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.all().filter(product=product)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    if avg_rating is not None:
        # round to the nearest 0.5 value
        avg_rating = round(avg_rating * 2) / 2

    if not request.user.is_authenticated:
        template = 'products/product_detail.html'
        context = {
            'product': product,
            'reviews': reviews,
            'avg_rating': avg_rating,
        }
        return render(request, template, context)

    else:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        # find a match to the product and user
        wishlist = WishList.objects.filter(
                   user_profile=user_profile, product=product_id)

        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                reviews.create(
                    user_profile=user_profile,
                    product=product,
                    rating=request.POST.get('rating'),
                    review=request.POST.get('review'))
                # re-filter reviews including the newest, and grab updated
                # aggregate rating
                reviews = Review.objects.all().filter(product=product)
                avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
                product.rating = avg_rating
                product.save()
                messages.info(request, 'Successfully added review.')
                return redirect(reverse('product_detail', args=[product_id]))
            else:
                messages.error(request, 'Failed to add review. \
                        Please check the form is valid and try again.')
        else:
            form = ReviewForm()

        template = 'products/product_detail.html'
        context = {
            'form': form,
            'product': product,
            'user_profile': user_profile,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'wishlist': wishlist,
        }

        return render(request, template, context)

@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))