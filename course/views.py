from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Course
from .serializers import CourseSerializer
from user.serializers import StudentSerializer
from user.models import BaseUser
from user.permissions import IsAdminUser, IsStudentUser

# Admin Routes
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def course_list(request):
    if request.method == 'GET':
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        if request.user.role == 'Admin':
            course_data = []
            for course in courses:
                students = course.students.all()
                course_serializer = CourseSerializer(course)
                student_serializer = StudentSerializer(students, many=True)

                course_data.append({
                    'name': course_serializer.data['name'],
                    'credit_hours': course_serializer.data['credit_hours'],
                    'students': student_serializer.data,
                })

            return Response({ 'message': 'Data retrieved successfully', 'data': course_data }, status=status.HTTP_200_OK)
        return Response({ 'message': 'Data retrieved successfully', 'data': serializer.data }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if request.user.role == 'Admin':
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Students are not allowed to create courses.'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Student Routes
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudentUser])
def student_courses(request):
    if request.method == 'GET':
        student = BaseUser.objects.get(email=request.user.email)
        if student:
            courses = student.courses.all()
            serializer = CourseSerializer(courses, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': 'Student not found.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudentUser])
def add_course_to_schedule(request, course_id):
    try:
        student = BaseUser.objects.get(email__exact=request.user.email)
        course = Course.objects.get(pk=course_id)
        new_total_credit_hours = student.hour_rate + course.credit_hours

        if new_total_credit_hours <= 30:
            student.courses.add(course)
            student.hour_rate = new_total_credit_hours
            student.save()

            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Adding this course exceeds the maximum credit hours.'}, status=status.HTTP_400_BAD_REQUEST)

    except BaseUser.DoesNotExist:
        return Response({'error': 'Student not found.'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found.'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsStudentUser])
def remove_course_from_schedule(request, course_id):
    try:
        student = request.user
        course = Course.objects.get(id=course_id)
        if course in student.courses.all():
            student.courses.remove(course)
            student.hour_rate -= course.credit_hours
            student.save()
            return Response({'message': 'Course removed from schedule'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Course is not in the schedule'}, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
