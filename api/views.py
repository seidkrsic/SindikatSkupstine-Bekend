from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from api import serializers
from api.serializers import CompanySerializer, ImportantDocumentSerializer, NewsSerializer, NewsSerializerForSlides, ProfileSerializer, SessionSerializer
from sindikat_app.models import Company, Image, Document, Agenda_Item, ImportantDocument, News, Session, CompanyDocument
from user_app.models import Profile 
from .pagination import NewsPagination 
from django.http import FileResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.files import File
import mimetypes
# Create your views here.


@api_view(["GET"])
def getRoutes(request): 
    routes = [ 
        "api/token", 
        "api/refreshtoken",
    ]
    return Response(routes)



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['boardMember'] = user.profile.board_member
       

        return token
class MyTokenObtainPairView(TokenObtainPairView): 
    serializer_class = MyTokenObtainPairSerializer



@api_view(["GET"])
def getNews(request): 
    news = News.objects.all()[:3]
    serializers = NewsSerializer(instance=news, many=True)
    return Response(serializers.data) 


@api_view(["GET"])
def getCompany(request): 
    companies = Company.objects.all() 
    serializers = CompanySerializer(instance=companies, many=True)
    return Response(serializers.data)



@api_view(["GET"])
def getNewsForSlides(request): 
    news = News.objects.filter(main=True)[:3]
    serializers = NewsSerializerForSlides(instance=news, many=True)
    return Response(serializers.data)


@api_view(["GET"])
def getSingleNews(request, pk): 
    news = News.objects.get(id=pk)
    serializers = NewsSerializer(instance=news, many=False)
    return Response(serializers.data)

@api_view(["POST"]) 
def getFilteredNews(request): 
    search = request.data['search']
    print(search) 
    matching_news = News.objects.filter(title__icontains=search)
    if matching_news: 
        serializers = NewsSerializer(instance=matching_news, many=True) 
        return Response(serializers.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def getSessions(request): 
    try: 
        category = request.GET.get("name")
    except: 
        category = None

    queryset = Session.objects.all()  # Get all News objects
  
    if category is not None:
        queryset = queryset.filter(category=category) 
    serializer = SessionSerializer(instance=queryset, many=True) 
    return Response(serializer.data)


@api_view(["GET"])
def getSession(request, pk): 
    try: 
        session = Session.objects.get(id=pk) 
    except: 
        return Response("No Session object with given id.")
    serializer = SessionSerializer(instance=session, many=False) 
    if session: 
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def importantDocuments(request): 
    documents = ImportantDocument.objects.all()
    serializer = ImportantDocumentSerializer(instance=documents, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_important_documents(request):
    important_documents = ImportantDocument.objects.filter(important=True)[:5]
    serializer = ImportantDocumentSerializer(instance=important_documents, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_all_documents(request):
    try: 
        category = request.GET.get("name")
    except: 
        category = None
    important_documents = ImportantDocument.objects.all()
    if category is not None and category in ["laws", "legislation", "regulations", "other"]:  
        if category == "legislation": 
            queryset = important_documents.filter(legislation=True)
        elif category == "laws": 
            queryset= important_documents.filter(laws=True)
        elif category == "regulations": 
            queryset = important_documents.filter(regulations=True)
        elif category == "other": 
            queryset = important_documents.filter(other=True)
        if category:
            serializer = ImportantDocumentSerializer(instance=queryset, many=True)
            return Response(serializer.data)
        return Response("Not valid filter.")

    return Response("No documents in db.")


@api_view(['GET'])
def download_important_document(request, pk):
    try: 
        document = ImportantDocument.objects.get(id=pk)
    except: 
     
        try: 
            document = Document.objects.get(id=pk)
        except: 
            try: 
                document = CompanyDocument.objects.get(id=pk)
            except: 
                return Response("Document not Found.")
        

    file_path = document.file.path

    # Koristimo `File` da dobijemo `content_type`
    mime_type, _ = mimetypes.guess_type(file_path)


    # Koristimo `FileResponse` sa postavljenim zaglavljima
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, content_type=mime_type)
    response['Content-Disposition'] = f'attachment; filename="{document.title}"'

    return response





@api_view(["GET"])
def get_board_members(request): 
    board_members = Profile.objects.filter(board_member=True).order_by('username')
    serializer = ProfileSerializer(instance=board_members, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_commission(request): 
    commission = Profile.objects.filter(commission=True).order_by('username')
    serializer = ProfileSerializer(instance=commission, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_presidents(request): 
    presidents = Profile.objects.filter(president=True).order_by('username')
    serializer = ProfileSerializer(instance=presidents, many=True)
    return Response(serializer.data)

@api_view(["GET"]) 
def get_profile(request, pk): 
    profile = Profile.objects.get(id=pk) 
    serializer = ProfileSerializer(instance=profile, many=False) 
    return Response(serializer.data) 

@api_view(["GET"]) 
def get_president(request): 
    profile = Profile.objects.filter(active_president=True).first()
    serializer = ProfileSerializer(instance=profile, many=False) 
    return Response(serializer.data) 


@api_view(["GET"]) 
def get_vice_president(request): 
    profile = Profile.objects.filter(vice_president=True).first()
    serializer = ProfileSerializer(instance=profile, many=False) 
    return Response(serializer.data) 

@api_view(["GET"]) 
def get_main_board_members(request): 
    profile = Profile.objects.filter(main_board_member=True).order_by("username")
    if profile: 
        serializer = ProfileSerializer(instance=profile, many=True) 
        return Response(serializer.data) 
    return Response({"No entries in db."})



@api_view(['GET'])
def get_paginated_news(request):
    queryset = News.objects.all()  # Get all News objects

    # category = request.GET.get('category')
    # if category:
    #     queryset = queryset.filter(category=category) 
    # # Apply the custom pagination
    paginator = NewsPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    # Serialize the paginated queryset
    serializer = NewsSerializer(paginated_queryset, many=True)  # Replace with your serializer

    # Return the paginated response
    return paginator.get_paginated_response(serializer.data) 










