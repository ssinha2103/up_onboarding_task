from rest_framework import permissions

from .models import Restaurant, Food, Order


class MerchantPermission(permissions.BasePermission):
    """
    Check if the user is a restaurant merchant.
    """

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.profile.is_merchant


class HasRestaurant(permissions.BasePermission):
    """
    Check if the merchant has created a restaurant to manage.
    """

    message = "You should create a restaurant first to be able to access it's foods"

    def has_permission(self, request, view):
        return bool(Restaurant.objects.filter(merchant=request.user.pk).first())


class IsFoodOwner(permissions.BasePermission):
    """
    Check if the merchant is the owner of the food which wants to edit.
    """

    message = "You are not the owner of this food restaurant"

    def has_permission(self, request, view):
        food = Food.objects.filter(pk=view.kwargs.get("pk", None)).first()
        if food is None:
            return False
        return (
            Restaurant.objects.filter(merchant=request.user.pk).first()
            == food.restaurant
        )


class CustomerCancellOrderPermission(permissions.BasePermission):
    """
    Check if the customer has the permission to cancell the order.
    """

    message = (
        "You don't have permission to cancel this order."
    )

    def has_permission(self, request, view):
        order = Order.objects.filter(pk=view.kwargs.get("pk", None)).first()
        if order is None:
            return False
        return not order.is_accepted and not order.is_cancelled


class IsCustomerOfOrder(permissions.BasePermission):
    """
    Check if the customer is the owner of order.
    """

    message = "You can't cancel this order because you are not it's owner."

    def has_permission(self, request, view):
        order = Order.objects.filter(customer=request.user.pk).first()
        return order is not None


class CustomerApproveDeliveredOrderPermission(permissions.BasePermission):
    """
    Check if the customer has permission to aprrove the delivered order.
    """

    message = "You can not approve this order as delivered."

    def has_permission(self, request, view):
        order = Order.objects.filter(pk=view.kwargs.get("pk", None)).first()
        if order is None:
            return False
        return order.is_accepted and not order.is_cancelled and not order.is_delivered


class IsMerchantOfOrder(permissions.BasePermission):
    """
    Check if the merchant is the owner of order.
    """

    message = "You are not the merchant of this order."

    def has_permission(self, request, view):
        order = Order.objects.filter(pk=view.kwargs.get("pk", None)).first()
        if order is None:
            return False
        food = order.foods.first()
        if order is None or food is None:
            return False
        return food.restaurant.merchant.pk == request.user.pk


class MerchantCancelAcceptOrderPermission(permissions.BasePermission):
    """
    Check if the merchant has permission to cancell the order.
    """

    message = "You don't have permission to cancel this order."

    def has_permission(self, request, view):
        order = Order.objects.filter(pk=view.kwargs.get("pk", None)).first()
        if order is None:
            return False
        return not order.is_cancelled and not order.is_accepted
