from aws_cdk import aws_apigateway as apigateway
from constructs import Construct
from utils.create_lambda import create_lambda_function


class ArtistsConstruct(Construct):
    def __init__(self, scope: Construct, id: str, api: apigateway.RestApi, authorizer, artists_table):
        super().__init__(scope, id)

        create_artist_lambda = create_lambda_function(
            self,
            "CreateArtistLambda",
            handler="handler.handler",
            include_dir="lambda/artist/create_artist",
            layers=[],
            environment={"ARTISTS_TABLE_NAME": artists_table.table_name}
        )
        artists_table.grant_read_write_data(create_artist_lambda)

        get_artists_lambda = create_lambda_function(
            self,
            "GetArtistsLambda",
            handler="handler.handler",
            include_dir="lambda/artist/get_artists",
            layers=[],
            environment={"ARTISTS_TABLE_NAME": artists_table.table_name}
        )
        artists_table.grant_read_data(get_artists_lambda)

        get_artist_lambda = create_lambda_function(
            self,
            "GetArtistLambda",
            handler="handler.handler",
            include_dir="lambda/artist/get_artist",
            layers=[],
            environment={"ARTISTS_TABLE_NAME": artists_table.table_name}
        )
        artists_table.grant_read_data(get_artist_lambda)

        update_artist_lambda = create_lambda_function(
            self,
            "UpdateArtistLambda",
            handler="handler.handler",
            include_dir="lambda/artist/update_artist",
            layers=[],
            environment={"ARTISTS_TABLE_NAME": artists_table.table_name}
        )
        artists_table.grant_read_write_data(update_artist_lambda)

        delete_artist_lambda = create_lambda_function(
            self,
            "DeleteArtistLambda",
            handler="handler.handler",
            include_dir="lambda/artist/delete_artist",
            layers=[],
            environment={"ARTISTS_TABLE_NAME": artists_table.table_name}
        )
        artists_table.grant_read_write_data(delete_artist_lambda)

        artists_resource = api.root.add_resource("artists")

        artists_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(
                get_artists_lambda,
                proxy=True,
                request_parameters={
                    "integration.request.querystring.genre": "method.request.querystring.genre"
                }
            ),
            request_parameters={"method.request.querystring.genre": False},
            # authorization_type=apigateway.AuthorizationType.COGNITO,
            # authorizer=authorizer
        )

        artists_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(create_artist_lambda, proxy=True),
            # authorization_type=apigateway.AuthorizationType.COGNITO,
            # authorizer=authorizer
        )

        artist_item_resource = artists_resource.add_resource("{id}")

        artist_item_resource.add_method(
            "GET",
            apigateway.LambdaIntegration(get_artist_lambda, proxy=True),
            # authorization_type=apigateway.AuthorizationType.COGNITO,
            # authorizer=authorizer
        )

        artist_item_resource.add_method(
            "PUT",
            apigateway.LambdaIntegration(update_artist_lambda, proxy=True),
            # authorization_type=apigateway.AuthorizationType.COGNITO,
            # authorizer=authorizer
        )
        
        artist_item_resource.add_method(
            "DELETE",
            apigateway.LambdaIntegration(delete_artist_lambda, proxy=True),
            # authorization_type=apigateway.AuthorizationType.COGNITO,
            # authorizer=authorizer
        )

