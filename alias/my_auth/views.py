from drf_yasg.utils import swagger_auto_schema
from my_auth.authentication import AuthenticationBySession
from my_auth.request import AuthenticatedRequest
from my_auth.serializers import UserSerializer, UserUpdateSerializer
from my_auth.services.user_crud import UserLogic
from rest_framework.response import Response
from rest_framework.views import APIView


class GetOrUpdateUserView(APIView):
    authentication_classes = [AuthenticationBySession]
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Get User",
        responses={"200": serializer_class()},
    )
    def get(self, request: AuthenticatedRequest) -> Response:
        user = request.user
        return Response(self.serializer_class(user).data, status=200)

    @swagger_auto_schema(
        operation_description="Update User",
        request_body=UserUpdateSerializer(),
        responses={"200": serializer_class()},
    )
    def patch(self, request: AuthenticatedRequest) -> Response:
        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        UserLogic.update_user(user, serializer.validated_data)
        return Response(self.serializer_class(user).data, status=200)
