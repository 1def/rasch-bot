#!/usr/bin/env python3
import json, subprocess, tempfile, os, csv, datetime as dt
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def normalize_matrix(matrix):
    if not matrix or not matrix[0]:
        raise ValueError("Matrix bosh)
    rows, cols = len(matrix), len(matrix[0])
    for row in matrix:
        if len(row) != cols:
            raise ValueError(Matrix
