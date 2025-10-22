from aws_cdk import Stack
from aws_cdk import aws_dynamodb as dynamodb
from constructs import Construct


class BackendStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        genre_table = dynamodb.Table(
            self, "GenreTable",
            table_name="songify-genres",
            partition_key=dynamodb.Attribute(
                name="genre_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )

        artists_table = dynamodb.Table(
            self, "ArtistsTable",
            table_name="songify-artists",
            partition_key=dynamodb.Attribute(
                name="genre_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="artist_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )
        artists_table.add_global_secondary_index(
            index_name="ArtistIDIndex",
            partition_key=dynamodb.Attribute(
                name="artist_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )

        albums_table = dynamodb.Table(
            self, "AlbumsTable",
            table_name="songify-albums",
            partition_key=dynamodb.Attribute(
                name="artist_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="album_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )
        albums_table.add_global_secondary_index(
            index_name="AlbumIDIndex",
            partition_key=dynamodb.Attribute(
                name="album_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )

        tracks_table = dynamodb.Table(
            self, "TracksTable",
            table_name="songify-tracks",
            partition_key=dynamodb.Attribute(
                name="album_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="track_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )
        tracks_table.add_global_secondary_index(
            index_name="AlbumIndex",
            partition_key=dynamodb.Attribute(
                name="album_id",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="track_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )
        tracks_table.add_global_secondary_index(
            index_name="SongIDIndex",
            partition_key=dynamodb.Attribute(
                name="track_id",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=1,
            write_capacity=1
        )
