Title: Adding Custom Javascript to the IPython Environment
date: 2014-10-21
comments: true
slug: ipython-javascript

I've been working on learning [D3.js](http://d3js.org/) for data visualization work at MD Anderson.
To speed development, one thing I wanted to do was include d3.js in every document so I didn't have to load 
it manually.
This was a bit tricky.
First, I located where the IPython configuration directory is;
on UNIX like systems, this is `~/.ipython/profile_default`.
Inside this directory, we are interested in the `static/custom` directory.
There, we place the [minimized D3.js file](https://raw.githubusercontent.com/mbostock/d3/master/d3.min.js) named `d3.min.js`.

    $([IPython.events]).on('app_initialized.NotebookApp', function(){
        require(['/static/custom/d3.min.js'], function(loader){
            loader.parameters('dummy');
            console.log('D3.js loaded');
        });
    });

As a result, you can now run D3.js examples without having to include any foreign scripts;
for example, copying the [first tutorial example](http://bost.ocks.org/mike/bar/), we can simply have a cell execute
the following code and have the corresponding bar plot rendered.

    from IPython.display import HTML
    s = """<!DOCTYPE html>
    <meta charset="utf-8">
    <style>
    
    .chart div {
      font: 10px sans-serif;
      background-color: steelblue;
      text-align: right;
      padding: 3px;
      margin: 1px;
      color: white;
    }
    
    </style>
    <div class="chart"></div>
    <script>
    
    var data = [4, 8, 15, 16, 23, 42];
    
    var x = d3.scale.linear()
        .domain([0, d3.max(data)])
        .range([0, 420]);
    
    d3.select(".chart")
      .selectAll("div")
        .data(data)
      .enter().append("div")
        .style("width", function(d) { return x(d) + "px"; })
        .text(function(d) { return d; });
    
    </script>"""
    h = HTML(s); h


