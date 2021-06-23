from dashboard.functions import *
from dashboard.skills import *
from authpage.views import *
from authpage.eee import *
from authpage.mech import *
from authpage.ece import *
from authpage.cse import *
from authpage.models import Student
from django.contrib import messages
from dashboard.models import *
from django.core.files.storage import FileSystemStorage
import numpy as np
from matplotlib import pyplot as plt
from django.shortcuts import render, redirect
import random
import matplotlib
matplotlib.use('Agg')
