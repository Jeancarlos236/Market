from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Product
# only for function based views
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.views.generic.edit import CreateView
# works for class based views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
# Create your views here.


def index(request):
    return HttpResponse("Hello World")


# function based view for listing
'''
def products(request):
    products = Product.objects.all()
    #if you want to use pagination in function use the paginator module
    context = {
        'products': products
    }
    return render(request, 'app/index.html', context)
'''

# class based view for above products view [ListView]


class ProductListView(ListView):
    model = Product
    template_name = 'app/index.html'
    context_object_name = 'products'
    paginate_by = 3


'''
def product_detail(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'app/detail.html', context)
'''

# class based view for product_detail [DetailView]


class ProductDetailView(DetailView):
    model = Product
    template_name = 'app/detail.html'
    context_object_name = 'product'


'''
@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        desc = request.POST.get('desc')
        image = request.FILES['upload']
        seller_name = request.user
        product = Product(name=name, price=price, desc=desc,image=image, seller_name=seller_name)
        product.save()
    return render(request, 'app/addproduct.html')

'''
# Class based view for creating a product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'price', 'desc', 'image']
    # success_url = reverse_lazy('app:products')

    def form_valid(self, form):                     
        form.instance.seller_name = self.request.user
        return super().form_valid(form)


'''
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.desc = request.POST.get('desc')
        # If you want to keep the old photo don't need to reupload
        if request.FILES.get('upload'):
            product.image = request.FILES['upload']
        # save to DB
        product.save()
        return redirect('/app/products')
    context = {
        'product': product,
    }
    return render(request, 'app/updateproduct.html', context)
'''

# Class based view for updating


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    # Specify the fields to include in the form
    fields = ['name', 'price', 'desc', 'image']
    template_name = 'app/product_update_form.html'  # Update the template name
    success_url = reverse_lazy('app:products')

    def dispatch(self, request, *args, **kwargs):
        # Get the product object being updated
        product = self.get_object()

        # Check if the logged-in user is the same as the product's seller
        if request.user != product.seller_name:
            raise Http404("You are not authorized to edit this product.")

        return super().dispatch(request, *args, **kwargs)


'''
def delete_product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product,
    }
    if request.method == 'POST':
        product.delete()
        return redirect('/app/products')
    return render(request, 'app/delete.html', context)
'''
# class based view for product deletion


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('app:products')

    def dispatch(self, request, *args, **kwargs):
        # Get the product object being updated
        product = self.get_object()

        # Check if the logged-in user is the same as the  seller
        if request.user != product.seller_name:
            raise Http404(
                "You are not authorized to Delete or edit this product.")

        return super().dispatch(request, *args, **kwargs)


def my_listing(request):
    products = Product.objects.filter(seller_name=request.user)
    context = {
        'products': products,
    }
    return render(request, 'app/mylistings.html', context)


class SearchView(ListView):
    model = Product
    template_name = 'app/search_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Product.objects.filter(name__icontains=query)
