from django.db import models

# Create your models here.


class Song(models.Model):
    # This is your index column from the command
    idx = models.IntegerField(primary_key=True)

    # "id" column from DB – renamed to avoid confusion with Django's default pk
    song_id = models.CharField(max_length=64, db_column="id")

    title = models.CharField(max_length=255)
    danceability = models.FloatField()
    energy = models.FloatField()
    key = models.IntegerField()
    loudness = models.FloatField()
    mode = models.IntegerField()
    acousticness = models.FloatField()
    instrumentalness = models.FloatField()
    liveness = models.FloatField()
    valence = models.FloatField()
    tempo = models.FloatField()
    duration_ms = models.IntegerField()
    time_signature = models.IntegerField()
    num_bars = models.IntegerField()
    num_sections = models.IntegerField()
    num_segments = models.IntegerField()

    # "class" is a Python keyword, so we give it a safe field name
    song_class = models.IntegerField(db_column="class")

    class Meta:
        managed = False
        db_table = "songs_normalized"  # existing SQLite table name

    def __str__(self):
        return f"{self.idx} - {self.title}"
