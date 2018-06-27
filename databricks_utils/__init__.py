"""
Ease-of-use tools for databricks notebooks.

.. moduleauthor:: eterna2@hotmail.com
"""
if 'displayHTML' not in locals():
    from IPython.core.display import display, HTML
    # Hack to make `displayHTML` work in both databricks and jupyter notebook.
    displayHTML = lambda x: display(HTML(x)) # pylint: disable=invalid-name
    """
    Alias for `displayHTML` in databricks notebooks and `display(HTML(...))` in jupyter notebooks.

    :param x: HTML string to be rendered.
    """

__all__ = ["displayHTML"]
