from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse, reverse_lazy

from .models import Restaurant, Food, Order

from .serializers import (
    UserSerializer,
    LoginSerializer,
    RestaurantSerializer,
    CreateRestaurantSerializer,
    FoodSerializer,
    PlaceOrderSerializer,
    CancellOrderSerializer,
    ApproveDeliveredOrderSerializer,
    AcceptOrderSerializer,
)

from .permissions import (
    MerchantPermission,
    HasRestaurant,
    IsFoodOwner,
    CustomerCancellOrderPermission,
    IsCustomerOfOrder,
    CustomerApproveDeliveredOrderPermission,
    IsMerchantOfOrder,
    MerchantCancelAcceptOrderPermission,
)

# Customers API URI
# path("customer/neworder/", CreateOrder.as_view(), name="customer_new_order"),
# path("customer/activeorders/", CustomerActiveOrderList.as_view(), name="customer_active_orders"),
# path(
#     "customer/cancelledorders/",
#     CustomerCancelledOrderList.as_view(), name="customer_cancelled_orders"),
# # path(
# #     "customer/deliveredorders/",
# #     CustomerDeliveredOrderList.as_view(), name="customer_new_order" ),
# path("customer/cancel/<int:pk>/", CustomerCancellOrder.as_view(), name="customer_cancel_order"),
#
#
# # path(
# #     "customer/approvedelivered/<int:pk>/",
# #     CustomerAprroveDeliveredOrder.as_view(), name="customer_new_order"
# # ),

@api_view(['GET'])
def ApiHomepage(request, format=None):
    return Response({
        # General API URI
        'register': reverse_lazy('register', request=request, format=format),
        'login': reverse_lazy('login', request=request, format=format),
        'logout': reverse_lazy('logout', request=request, format=format),
        'users': reverse_lazy('users', request=request, format=format),
        'profile': reverse_lazy('profile', request=request, format=format),
        'restaurants': reverse_lazy('restaurants', request=request, format=format),

        # Merchant API URI
        'merchant_create_new_restaurants': reverse_lazy('merchant_create_new_restaurants', request=request, format=format),
        'merchant_create_new_food_list': reverse_lazy('merchant_create_new_food_list', request=request, format=format),
        #'merchant_update_food_list': reverse_lazy('merchant_update_food_list', args=[], request=request, format=format),
        'merchant_active_orders': reverse_lazy('merchant_active_orders', request=request, format=format),
        'merchant_cancelled_orders': reverse_lazy('merchant_cancelled_orders', request=request, format=format),
        #'merchant_cancel_order': reverse_lazy('merchant_cancel_order', request=request, format=format),
        #'merchant_accept_order': reverse_lazy('merchant_accept_order', request=request, format=format),
        'merchant_delivered_orders': reverse_lazy('merchant_delivered_orders', request=request, format=format),

        # Customer API URI

        'customer_new_order': reverse_lazy('customer_new_order', request=request, format=format),
        'customer_active_orders': reverse_lazy('customer_active_orders', request=request, format=format),
        'customer_cancelled_orders': reverse_lazy('customer_cancelled_orders', request=request, format=format),
        #'customer_cancel_order': reverse_lazy('customer_cancel_order', request=request, format=format),
        'customer_delivered_order': reverse_lazy('customer_delivered_order', request=request, format=format),


    })


class api_login(generics.CreateAPIView):
    """
    Login user with username and password.
    """

    serializer_class = LoginSerializer

    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_logout(request):
    request.session.flush()
    return Response(status=status.HTTP_200_OK)


class Register(generics.CreateAPIView):
    """
    Register a new account.
    """

    serializer_class = UserSerializer


class UserList(generics.ListCreateAPIView):
    """
    Show list of all users or create a new user.
    """

    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfile(generics.RetrieveUpdateDestroyAPIView):
    """
    User profile to be retrieved, updated or destroyed.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return User.objects.filter(pk=self.request.user.pk).first()


class RestaurantList(generics.ListAPIView):
    """
    List of all restaurants.
    """

    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()


class CreateRestaurant(generics.CreateAPIView):
    """
    Create a restaurant by merchant.
    """

    serializer_class = CreateRestaurantSerializer
    permission_classes = (
        IsAuthenticated,
        MerchantPermission,
    )

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user)


class MerchantFoodListCreate(generics.ListCreateAPIView):
    """
    Create food for restaurant by merchant.
    """

    serializer_class = FoodSerializer
    permission_classes = (
        IsAuthenticated,
        MerchantPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(merchant=self.request.user.pk).first()
        return Food.objects.filter(restaurant=restaurant)

    def perform_create(self, serializer):
        restaurant = Restaurant.objects.filter(merchant=self.request.user.pk).first()
        serializer.save(restaurant=restaurant)


class UpdateFood(generics.UpdateAPIView):
    """
    Update food information and price.
    """

    serializer_class = FoodSerializer
    permission_classes = (
        IsAuthenticated,
        MerchantPermission,
        HasRestaurant,
        IsFoodOwner,
    )
    queryset = Food.objects.all()


class CreateOrder(generics.CreateAPIView):
    """
    Place an Order.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class CustomerActiveOrderList(generics.ListAPIView):
    """
    List of all active orders which are not cancelled or delivered.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(
            customer=self.request.user.pk, is_cancelled=False, is_delivered=False
        )


class CustomerCancelledOrderList(generics.ListAPIView):
    """
    List of customer's cancelled orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.pk, is_cancelled=True)


class CustomerDeliveredOrderList(generics.ListAPIView):
    """
    List of customer's delivered orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.pk, is_delivered=True)


class CustomerCancellOrder(generics.UpdateAPIView):
    """
    Cancell order if has permission to.
    """

    serializer_class = CancellOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsCustomerOfOrder,
        CustomerCancellOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


class CustomerAprroveDeliveredOrder(generics.UpdateAPIView):
    """
    Aprrove that order has been delivered.
    """

    serializer_class = ApproveDeliveredOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsCustomerOfOrder,
        CustomerApproveDeliveredOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(delivered_datetime=timezone.now())


class MerchantActiveOrderList(generics.ListAPIView):
    """
    List of merchant's restaurant active orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        MerchantPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(merchant=self.request.user.pk).first()
        foods = Food.objects.filter(restaurant=restaurant.pk).values_list("id").first()
        orders = Order.objects.filter(
            foods__in=foods, is_cancelled=False, is_delivered=False
        )
        return orders


class MerchantCancelledOrderList(generics.ListAPIView):
    """
    List of merchant's restaurant cancelled orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        MerchantPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(merchant=self.request.user.pk).first()
        foods = Food.objects.filter(restaurant=restaurant.pk).values_list("id").first()
        orders = Order.objects.filter(
            foods__in=foods, is_cancelled=True
        )
        return orders


class MerchantDeliveredOrderList(generics.ListAPIView):
    """
    List of merchant's restaurant delivered orders.
    """

    serializer_class = PlaceOrderSerializer
    permission_classes = (
        IsAuthenticated,
        MerchantPermission,
        HasRestaurant,
    )

    def get_queryset(self):
        restaurant = Restaurant.objects.filter(merchant=self.request.user.pk).first()
        foods = Food.objects.filter(restaurant=restaurant.pk).values_list("id").first()
        orders = Order.objects.filter(
            foods__in=foods, is_delivered=True
        )
        return orders


class MerchantCancelOrder(generics.UpdateAPIView):
    """
    Cancel order if has permission to.
    """

    serializer_class = CancellOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsMerchantOfOrder,
        MerchantCancelAcceptOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(cancell_datetime=timezone.now())


class MerchantAcceptOrder(generics.UpdateAPIView):
    """
    Accept order if has permission to.
    """

    serializer_class = AcceptOrderSerializer
    permission_classes = (
        IsAuthenticated,
        IsMerchantOfOrder,
        MerchantCancelAcceptOrderPermission,
    )
    queryset = Order.objects.all()

    def perform_update(self, serializer):
        serializer.save(accept_datetime=timezone.now())
