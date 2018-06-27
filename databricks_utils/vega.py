
"""
Basic vega functions to plot vega charts in databricks or jupyter notebooks.

.. moduleauthor:: eterna2@hotmail.com
"""
import json
import databricks_utils


DEFAULT_VEGA_OPTS = dict(theme="quartz",
                         defaultStyle=True,
                         actions=dict(export=True,
                                      source=True,
                                      editor=False,
                                      renderer="canvas"))
"""Default settings for `vega-embed` (See `https://github.com/vega/vega-embed`)."""


def vega_embed(spec, plot=True, **kwargs):
    """
    Display a vega chart. Also return the HTML to display the vega chart.

    :param plot: Set `True` to display vega chart on the notebook.
    :param kwargs:  See `https://github.com/vega/vega-embed` for the vega
                    embed settings.
    """
    tmp = dict()
    tmp.update(DEFAULT_VEGA_OPTS)
    tmp.update(kwargs)
    conf = json.dumps(tmp)

    if isinstance(spec, dict):
        spec = json.dumps(spec)

    html = """
    <!DOCTYPE html>
    <html>
        <head>
        <script src="https://cdn.jsdelivr.net/npm/vega@3"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-lite@2"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-embed@3"></script>
        <script src="https://cdn.jsdelivr.net/npm/vega-themes@2"></script>
        </head>
        <body>
            <div id="vis"></div>
            <script type="text/javascript">
                var spec = """+spec+""";
                vegaEmbed('#vis', spec, """+conf+""").catch(console.error);
            </script>
        </body>
    </html>"""

    if plot:
        databricks_utils.displayHTML(html) # pylint: disable=undefined-variable

    return html
