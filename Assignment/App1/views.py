from .models import Product, Leads
from .serializers import ProductSerializer, LeadSerializer,ProductSerializer1
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from django.db.models import Count
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):

        request_data = request.data
        kwargs = {}
        name = request_data.get("name","")
        product_id = request_data.get("product_id","")

        if name:
            kwargs["name__iexact"] = name
            
        if product_id:
            kwargs["id"] = product_id
        
        try:
            response_data = {}
            products = Product.objects.filter(**kwargs)
            if products.exists():
                serializerdata = ProductSerializer(products, many=True)
            else:
                products = Product.objects.all()
                serializerdata = ProductSerializer(products, many=True)
            response_data = {
                "True" : "success",
                "data" : serializerdata.data
            }
            return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


    def post(self, request):

        request_data = request.data
        kwargs = {}
        name = request_data.get("name","")
        description = request_data.get("description","")
        price = request_data.get("price","")


        if name:
            kwargs["name"] = name
    
        if description:
            kwargs["description"] = description

        if price:
            if price > 0:
                kwargs["price"] = price
            else:
                return Response(data={"msg":"please enter positive price"})
        
        try:
            Product.objects.create(**kwargs)
            return Response(data={"msg":"product object created successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
        
    
    def put(self, request):
        request_data = request.data
        try:
            product_id = request_data.get("product_id")

            obj = Product.objects.get(id=product_id)
            if obj:
                obj.name = request_data.get("name", obj.name)
                obj.description = request_data.get("description", obj.description)
                price = request_data.get("price",obj.price)
                if price < 0:
                    return Response(data={"msg":"please enter positive price"})
                
                obj.price = request_data.get("price",obj.price)
                obj.save()
                return Response(data={"msg":"Product updated successfully"},status=status.HTTP_200_OK)
            return Response(data={"msg":"Product does not exists"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        request_data = request.data
        try:
            product_id = request_data.get("product_id")
            obj = Product.objects.filter(id=product_id)
            if obj.exists():
                obj.delete()
                return Response(data={"msg":"object delete successfully"}, status=status.HTTP_200_OK)
            return Response(data={"msg":"object Does not Exists"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class LeadView(APIView):

    def post(self, request):
        request_data = request.data
        lead_name = request_data.get("lead_name"," ")
        email = request_data.get("email"," ")
        number = request_data.get("number"," ")
        product = request_data.get("product"," ")
        kwargs = {}
        try:
            if lead_name:
                kwargs["lead_name"] = lead_name
            
            if email:
                kwargs["email"] = email
            
            if number:
                kwargs["phone_number"] = number

            for pro in product:
                obj = Leads.objects.create(**kwargs)
                obj.product.add(pro)
                obj.save()
            return Response(data={"mag":"lead created successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)


class ReportingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        request_data = request.data

        from_dt = request_data.get("from_dt")
        to_dt = request_data.get("to_dt")
        most_lead = request_data.get("most_lead", "false").lower() == "true"
        Least_lead = request_data.get("Least_lead", "false").lower() == "true"
        product_id= request_data.get("product_id")
        kwargs = {}

        try:
            if from_dt:
                from_date = timezone.make_aware(datetime.strptime(f"{from_dt} 00:00:00", "%Y-%m-%d %H:%M:%S"))
                kwargs['created_at__gte'] = from_date

            if to_dt:
                to_date = timezone.make_aware(datetime.strptime(f"{to_dt} 23:59:00", "%Y-%m-%d %H:%M:%S"))
                kwargs['created_at__lte'] = to_date

            if most_lead:
                products_with_lead_counts = Product.objects.annotate(num_leads=Count('leads')).order_by("-num_leads")[:10]
                serializerdata = ProductSerializer1(products_with_lead_counts, many=True)
                return Response(serializerdata.data, status=status.HTTP_200_OK)
        
            if Least_lead:
                products_with_lead_counts = Product.objects.annotate(num_leads=Count('leads')).order_by('num_leads')[:10]
                serializerdata = ProductSerializer1(products_with_lead_counts, many=True)
                return Response(serializerdata.data, status=status.HTTP_200_OK)

            if product_id:
                product_with_lead_count = Product.objects.filter(id=product_id).annotate(num_leads=Count('leads')).first()
                serializerdata = ProductSerializer1(product_with_lead_count)
                return Response(serializerdata.data, status=status.HTTP_200_OK)

            obj = Product.objects.filter(**kwargs)
            serializerdata = ProductSerializer(obj, many=True)
            return Response(data= serializerdata.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)