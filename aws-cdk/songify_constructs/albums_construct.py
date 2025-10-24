from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from utils.create_lambda import create_lambda_function

class AlbumsConstruct(Construct):
    def __init__(self, scope: Construct, id: str, api: apigateway.RestApi, authorizer, albums_table, artists_table, content_created_topic):
        super().__init__(scope, id)

        create_album_lambda = create_lambda_function(
            self,
            "CreateAlbumLambda",
            handler="handler.handler",
            include_dir="lambda/album/create_album",
            layers=[],
            environment={"ALBUMS_TABLE_NAME": albums_table.table_name,
                         "CONTENT_CREATED_TOPIC_ARN": content_created_topic.topic_arn,}
        )
        albums_table.grant_read_write_data(create_album_lambda)
        content_created_topic.grant_publish(create_album_lambda)

        get_albums_lambda = create_lambda_function(
            self,
            "GetAlbumsLambda",
            handler="handler.handler",
            include_dir="lambda/album/get_albums",
            layers=[],
            environment={"ALBUMS_TABLE_NAME": albums_table.table_name, "ARTISTS_TABLE_NAME": artists_table.table_name}
        )
        albums_table.grant_read_data(get_albums_lambda)
        artists_table.grant_read_data(get_albums_lambda)

        get_album_lambda = create_lambda_function(
            self,
            "GetAlbumLambda",
            handler="handler.handler",
            include_dir="lambda/album/get_album",
            layers=[],
            environment={"ALBUMS_TABLE_NAME": albums_table.table_name, "ARTISTS_TABLE_NAME": artists_table.table_name}
        )
        albums_table.grant_read_data(get_album_lambda)
        artists_table.grant_read_data(get_album_lambda)

        update_album_lambda = create_lambda_function(
            self,
            "UpdateAlbumLambda",
            handler="handler.handler",
            include_dir="lambda/album/update_album",
            layers=[],
            environment={"ALBUMS_TABLE_NAME": albums_table.table_name}
        )
        albums_table.grant_read_write_data(update_album_lambda)

        delete_album_lambda = create_lambda_function(
            self,
            "DeleteAlbumLambda",
            handler="handler.handler",
            include_dir="lambda/album/delete_album",
            layers=[],
            environment={"ALBUMS_TABLE_NAME": albums_table.table_name}
        )
        albums_table.grant_read_write_data(delete_album_lambda)

        albums_resource = api.root.add_resource("albums")

        albums_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(
                get_albums_lambda,
                proxy=True,
                request_parameters={
                    "integration.request.querystring.genre": "method.request.querystring.genre"
                }
            ),
            request_parameters={"method.request.querystring.genre": False},
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        albums_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(create_album_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        album_item_resource = albums_resource.add_resource("{id}")

        album_item_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_album_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        album_item_resource.add_method(
            "PUT",
            apigateway.LambdaIntegration(update_album_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        album_item_resource.add_method(
            "DELETE",
            apigateway.LambdaIntegration(delete_album_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )
