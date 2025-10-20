resource "aws_dynamodb_table" "genres" {
  name           = "${var.project_name}-genres"
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity

  hash_key = "genre_id"

  attribute {
    name = "genre_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "artists" {
  name           = "${var.project_name}-artists"
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity

  hash_key  = "genre_id"
  range_key = "artist_id"

  attribute {
    name = "genre_id"
    type = "S"
  }

  attribute {
    name = "artist_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "albums" {
  name           = "${var.project_name}-albums"
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity

  hash_key  = "genre_id"
  range_key = "album_id"

  attribute {
    name = "genre_id"
    type = "S"
  }

  attribute {
    name = "album_id"
    type = "S"
  }
}

resource "aws_dynamodb_table" "songs" {
  name           = "${var.project_name}-songs"
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity

  hash_key  = "artist_id"
  range_key = "song_id"

  attribute {
    name = "artist_id"
    type = "S"
  }

  attribute {
    name = "song_id"
    type = "S"
  }

  attribute {
    name = "album_id"
    type = "S"
  }

  global_secondary_index {
    name            = "AlbumIndex"
    hash_key        = "album_id"
    range_key       = "song_id"
    projection_type = "ALL"
    read_capacity   = var.read_capacity
    write_capacity  = var.write_capacity
  }
}