import coreapi
import coreschema
from game_room.models import Comments
from game_room.serializers.comment import CreateCommentSerializer
from my_auth.authentication import AuthenticationBySession
from rest_framework.response import Response
from rest_framework.schemas.coreapi import AutoSchema
from rest_framework.views import APIView


class AddCommentView(APIView):
    schema = AutoSchema(
        manual_fields=[
            coreapi.Field(
                "my_extra_field",
                required=True,
                location="path",
                schema=coreschema.String(),
            ),
        ]
    )
    authentication_classes = [AuthenticationBySession]
    serializer_class = CreateCommentSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        Comments.objects.create(**serializer.validated_data)
        return Response({}, status=201)
