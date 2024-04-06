def clean_frame(frame):
    """
    Limpia y destruye todos los widgets dentro de un marco (frame).

    Args:
        frame (tkinter.Frame): El marco (frame) del cual deseas eliminar los widgets.
    """
    
    # Elimina todos los widgets en pantalla
    for widget in frame.winfo_children():
        widget.destroy()