from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from utils.create_lambda import create_lambda_function


class GenresConstruct(Construct):
    def __init__(self, scope: Construct, id: str, api: apigateway.RestApi, authorizer, genres_table):
        super().__init__(scope, id)

        get_genres_lambda = create_lambda_function(
            self,
            "GetGenresLambda",
            handler="handler.handler",
            include_dir="lambda/genre/getGenres",
            layers=[],
            environment={
                "GENRES_TABLE_NAME": genres_table.table_name
            }
        )
        genres_table.grant_read_data(get_genres_lambda)

        create_genre_lambda = create_lambda_function(
            self,
            "CreateGenreLambda",
            handler="handler.handler",
            include_dir="lambda/genre/createGenre",
            layers=[],
            environment={
                "GENRES_TABLE_NAME": genres_table.table_name
            }
        )
        genres_table.grant_read_write_data(create_genre_lambda)

        delete_genre_lambda = create_lambda_function(
            self,
            "DeleteGenreLambda",
            handler="handler.handler",
            include_dir="lambda/genre/deleteGenre",
            layers=[],
            environment={
                "GENRES_TABLE_NAME": genres_table.table_name
            }
        )
        genres_table.grant_write_data(delete_genre_lambda)

        genres_resource = api.root.add_resource("genres")

        genres_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_genres_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        genres_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(create_genre_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )

        genre_item_resource = genres_resource.add_resource("{genre}")

        genre_item_resource.add_method(
            "DELETE",
            apigateway.LambdaIntegration(delete_genre_lambda, proxy=True),
            authorization_type=apigateway.AuthorizationType.COGNITO,
            authorizer=authorizer
        )
