if (heartRate <= 5) {{
    heart.style.color = '#4B0082';
}} else if (heartRate > 5 && heartRate <= 35) {{
    heart.style.color = '#3498DB';
}} else if (heartRate > 35 && heartRate <= 120) {{
    heart.style.color = '#FF0000';
}} else if (heartRate > 120) {{
    heart.style.color = '#FFD700';
}} else {{
    heart.style.color = '#B0C4DE';
}}