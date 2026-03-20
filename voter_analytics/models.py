# File: voter_analytics/models.py
# Author: Ilay Guler (ilay2004@bu.edu), 3/20/2026
# Description: Defines our voter object, grabbed from a large CSV dataset. Load_data() adapts csv row-column entries into voter objects
from django.db import models
from pathlib import Path

# Create your models here.
class Voter(models.Model):
  lastname = models.TextField(blank=False)
  firstname = models.TextField(blank=False)
  street_number = models.IntegerField(blank=False)
  street_name = models.TextField(blank=False)
  apartment_number = models.TextField(blank=False)
  zip_code = models.TextField(blank=False)
  dob = models.DateField(blank=False)
  dor = models.DateField(blank=False)
  party_afil = models.TextField(blank=False) 
  precinct_num = models.TextField(blank=False) #Some precinct number can have letters in them

  v20state = models.BooleanField(blank=False)
  v21town = models.BooleanField(blank=False)
  v21primary = models.BooleanField(blank=False) 
  v22general = models.BooleanField(blank=False)
  v23town = models.BooleanField(blank=False)

  voter_score = models.IntegerField()

def load_data():
  app_dir = Path(__file__).resolve().parent
  file_path = app_dir / 'CS412-newton_voters.csv'
  filename = './CS412-newton_voter.csv'
  f = open(file_path)
  f.readline() # discard headers

  for line in f:
    fields = line.split(',')
    # show which value in each field
    '''
    print(f'fields={fields}')
    for i in range(len(fields)):
      print(f'fields[{i}] = {fields[i]}')
    '''
    try:
      voter_id = fields[0]
      for i, bool in enumerate(fields[11:16]):
        if bool == 'TRUE':
          fields[i+11] = True
        else:
          fields[i+11] = False
      print(fields[1:])
      result = Voter(
        lastname = fields[1],
        firstname = fields[2],
        street_number = fields[3],

        street_name = fields[4],
        apartment_number = fields[5],
        zip_code = fields[6],
        dob = fields[7],
        dor = fields[8],
        party_afil = fields[9],
        precinct_num = fields[10],


        v20state = fields[11],
        v21town = fields[12],
        v21primary = fields[13],
        v22general = fields[14],
        v23town = fields[15],

        voter_score = fields[16],
      )
      result.save()
      print("Saved voter to DB")
    except:
      print(f"Failed to save voter to DB at {voter_id}")
  print(len(Voter.objects.all()), "voters saved to DB")
  