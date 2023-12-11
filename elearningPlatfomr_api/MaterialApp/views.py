from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Material
from .serializers import MaterialSerializer
from rest_framework.permissions import IsAuthenticated
from courseApp.models import Course 
from rest_framework.serializers import ValidationError
from django.http import Http404

from .permissions import CanUploadMaterialPermission , IsCourseTutor
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from .forms import MaterialForm
from django.template.response import TemplateResponse
# Create your views here.


class AddMaterialView(APIView):
    permission_classes = [IsAuthenticated , CanUploadMaterialPermission , IsCourseTutor]

    def get_course(self, course_id):
        try:
            return Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            raise ValidationError('Course with the specified ID does not exist.')

    def post(self, request, *args, **kwargs):
        course_id = self.kwargs.get('course_id')
        course = self.get_course(course_id)
        print ("course_id: ", course_id)

        try:
            serializer = MaterialSerializer(data=request.data)
            print(" serializer: ", serializer)
            if serializer.is_valid():
                serializer.validated_data['course'] = course
                serializer.save(course=course)
                return Response({'detail': 'Material added successfully.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data provided for material creation.'}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied:
            return Response({'error': 'You do not have permission to  create a material for this course'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateMaterialView(generics.UpdateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, CanUploadMaterialPermission]
    lookup_field = 'pk' 
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.check_object_permissions(request, instance)
            
            form = MaterialForm(initial={
                'title': instance.title,
                'content': instance.content,
                'upload_date': instance.upload_date,
                'document_type': instance.document_type,
                'course': instance.course
                
            })
            context = {'Material': instance, 'form': form, 'materialId': instance.pk ,'courseId': instance.course.id}
            
            # Render the template for the GET request
            template_name = 'update_Material.html' 
            return TemplateResponse(request, template_name, context)

        except PermissionDenied:
            return Response({'error': 'You do not have permission to update this course.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, *args, **kwargs):
        material_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(material_or_response, Response):
            return material_or_response

        material = material_or_response

        print("request user:", request.user)
        print("material course tutor id:", material.course.tutor.id)

        # Check if the requesting user is the tutor of the course
        if request.user != material.course.tutor:
            error_msg = "You do not have permission to update this material."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(material, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'detail': 'Material updated successfully.'}, status=status.HTTP_200_OK)


class DeleteMaterialView(generics.DestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated, CanUploadMaterialPermission]

    def get_object(self):
        material_id = self.kwargs.get('material_id')
        try:
            return get_object_or_404(Material, pk=material_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Material  did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        material_or_response = self.get_object()

        # Check if the result is a Response object
        if isinstance(material_or_response, Response):
            return material_or_response

        material = material_or_response

        print("request user:", request.user)
        print("material course tutor id:", material.course.tutor.id)

        # Check if the requesting user is the tutor of the course
        if request.user != material.course.tutor:
            error_msg = "You do not have permission to update this material."
            return Response({'error': error_msg}, status=status.HTTP_403_FORBIDDEN)


        material.delete()
        return Response({'detail': 'Material deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

class ListMaterialView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MaterialSerializer

    def get_queryset(self):
        course_id = self.kwargs.get('course_id')
        return Material.objects.filter(course_id=course_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
         # Get the course ID from the URL parameters
        course_id = self.kwargs.get('course_id')

        return render(request, 'materials.html', {'materials': serializer.data, 'user': request.user, 'course_id': course_id})

class MaterialDetailView(generics.RetrieveAPIView):
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated ]

    def get_object(self):
        material_id = self.kwargs.get('material_id')
        try:
            return get_object_or_404(Material, pk=material_id)
        except Http404:
            # Customize the response when material_id doesn't exist
            return Response({'error': 'Material did not exist'}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Render the HTML template with the serialized data
        return render(request, 'material_detail.html', {'material': serializer.data})