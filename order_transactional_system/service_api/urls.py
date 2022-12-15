from rest_framework import routers
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from rest_framework.schemas import get_schema_view
from .views import *

urlpatterns = [
    # rest_framework Authentication
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # OpenAPI and Swagger UI for API documentations
    # path(
    #     "openapi",
    #     get_schema_view(
    #         title="Food Ordering Service API",
    #         description="API documentation for every accessable url to you",
    #         version="1.0.0",
    #     ),
    #     name="openapi-schema",
    # ),
    # path(
    #     "documentation/",
    #     TemplateView.as_view(
    #         template_name="swagger-ui/swagger-ui.html",
    #         extra_context={"schema_url": "openapi-schema"},
    #     ),
    #     name="swagger-ui",
    # ),
    # Homepage
    path("", ApiHomepage),

    # General API URI
    path("register/", Register.as_view(), name='register'),
    path("login/", api_login.as_view(), name='login'),
    path("logout/", api_logout, name='logout'),
    path("users/", UserList.as_view(), name='users'),
    path("profile/", UserProfile.as_view(), name='profile'),
    path("restaurants/", RestaurantList.as_view(), name='restaurants'),
    # Merchant API URI
    path("merchant/newrestaurant/", CreateRestaurant.as_view(), name='merchant_create_new_restaurants'),
    path("merchant/foods/", MerchantFoodListCreate.as_view(), name='merchant_create_new_food_list'),
    path("merchant/updatefood/<int:pk>/", UpdateFood.as_view(), name='merchant_update_food_list'),
    path("merchant/activeorders/", MerchantActiveOrderList.as_view(), name='merchant_active_orders'),
    path("merchant/cancelledorders/",
         MerchantCancelledOrderList.as_view(), name='merchant_cancelled_orders'
         ),
    path(
        "merchant/deliveredorders/",
        MerchantDeliveredOrderList.as_view(), name='merchant_delivered_orders'),
    path("merchant/cancel/<int:pk>/", MerchantCancelOrder.as_view(), name='merchant_cancel_order'),
    path("merchant/accept/<int:pk>/", MerchantAcceptOrder.as_view(), name='merchant_accept_order'),
    # Customers API URI
    path("customer/neworder/", CreateOrder.as_view(), name="customer_new_order"),
    path("customer/activeorders/", CustomerActiveOrderList.as_view(), name="customer_active_orders"),
    path(
        "customer/cancelledorders/", CustomerCancelledOrderList.as_view(), name="customer_cancelled_orders"),
    path(
        "customer/deliveredorders/",
        CustomerDeliveredOrderList.as_view(), name="customer_delivered_order" ),
    path("customer/cancel/<int:pk>/", CustomerCancellOrder.as_view(), name="customer_cancel_order"),
    path(
        "customer/approvedelivered/<int:pk>/",
        CustomerAprroveDeliveredOrder.as_view(), name="customer_new_order"
    ),
]
