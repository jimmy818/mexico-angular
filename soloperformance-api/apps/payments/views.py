from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext as _
from rest_framework import exceptions, generics, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from performance.settings import getenvar
from apps.security import models as security_model
from apps.security import serializers as security_serializer

import json
import stripe


class StripeMixin(object):

    @property
    def stripe(self):
        secret = getenvar('STRIPE_TEST_SECRET_KEY')
        api_keys = json.loads(secret)

        if not self.request.user.region:
            raise exceptions.ValidationError(_("This user does not have an assigned region"))

        stripe.api_key = api_keys[self.request.user.region.name]
        return stripe


class ListProductsView(StripeMixin, generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        return Response(self.stripe.Product.list(active=True))


class RetrieveProductView(StripeMixin, generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        prod_id = kwargs.get('pk', '')

        try:
            product = self.stripe.Product.retrieve(prod_id)
        except Exception as e:
            raise exceptions.ValidationError(e.error.get('message'))

        return Response(product)


class ListProductPricesView(StripeMixin, generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        prod_id = kwargs.get('pk', '')

        try:
            prices = self.stripe.Price.list(active=True, product=prod_id)
        except Exception as e:
            raise exceptions.ValidationError(e.error.get('message'))

        return Response(prices)


class RetrievePriceView(StripeMixin, generics.RetrieveAPIView):

    def retrieve(self, request, *args, **kwargs):
        price_id = kwargs.get('pk', '')

        try:
            product = self.stripe.Price.retrieve(price_id)
        except Exception as e:
            raise exceptions.ValidationError(e.error.get('message'))

        return Response(product)


class CustomerView(generics.UpdateAPIView):
    queryset = security_model.User.objects.all()
    serializer_class = security_serializer.UserDetailSerializer

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
