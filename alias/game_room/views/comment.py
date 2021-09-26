from drf_yasg.utils import swagger_auto_schema
from game_room.models import Comments
from game_room.serializers.comment import CreateCommentSerializer
from my_auth.authentication import AuthenticationBySession
from rest_framework.response import Response
from rest_framework.views import APIView


class AddCommentView(APIView):
    authentication_classes = [AuthenticationBySession]
    request_serializer_class = CreateCommentSerializer

    @swagger_auto_schema(
        operation_description="Creating comment",
        request_body=request_serializer_class(),
        responses={"200": ""},
    )
    def post(self, request):
        serializer = self.request_serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        Comments.objects.create(**serializer.validated_data)
        return Response({}, status=201)
