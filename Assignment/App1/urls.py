from django.urls import path
from .views import ProductView, LeadView, ReportingView

urlpatterns = [
    path("productcrud/", ProductView.as_view(), name="product_ulr"),
    path("leadcreate/", LeadView.as_view(), name="leads_url"),
    path("reports/", ReportingView.as_view(), name='reportings_url')
]