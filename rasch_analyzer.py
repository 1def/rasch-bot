#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import subprocess
import tempfile
import os
import csv
import datetime as dt
from io import BytesIO
from typing import List, Dict, Any, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

def normalize_matrix(matrix: List[List[Any]]) -> List[List[int]]:
    """Matrixni 0/1 formatga otkazish
    if not matrix or not matrix[0]:
        raise ValueError(Matrix
