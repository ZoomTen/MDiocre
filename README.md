# MDiocre - an Amazing Project

![MDiocre](logo.svg)

A very simple static website generator tool powered by Python, Markdown (but can be extended to other markup)

## Requirements

* Python 3 (python-markdown, shutil)

If you want to build the documentation, you will have to install Sphinx as well.

## What sets it apart from other tools?

It's terrible and it doesn't have a profitable and pragmatic usecase in mind, but it works okay. For my needs, anyway. It's alright for simple blogs with no tagging and very simple static websites.

## How do I make a site with this?

1. After cloning/downloading this repo (extracting it to a folder called `MDiocre`), create a work folder adjacent to that folder. Let's call it `work`.

2. Make a file called `template.html` inside that folder with these contents:
   
   ```
   <html>
   <head>Welcome to my website!</head>
   <body><!--:content--></body>
   </html>
   ```

3. Create a folder called `src`, and make a file inside of it called `index.md`, and write anything on it.

4. After your content (or before, it doesn't matter), add: `<!--:mdiocre-template="../template.html"-->`

5. Go back a level to your `work` folder. Assuming Python is present in your PATH (environment variable), create a new text document containing:
   
   ```
   python3 ../MDiocre/mdiocre.py src build
   ```
   
   Save it inside the folder as a .bat if you're on Windows, or as a .sh if you're on Mac, Linux, or other Unix-like systems. Double click or execute it.

6. Check the `build` folder.

## Variables

MDiocre allows setting variables. These variables are per-page, and can be read by the template. Both the template and the markdown page share the same format for templates - which are HTML comments with the first character after the markup being the colon (:)

**Setting a variable to a string**

```
<!--: hello = "test message" -->
```

Simply sets `hello` to `test message`. When using a comma, make sure to escape it with \\!

**Setting a variable to another variable**

```
<!--: hello = lemons -->
```

If `lemons` is `1` then `hello` will also be `1`. If `lemons` is not set, `hello` will contain the string `lemons`.

**Concatenating two or more variables**

```
<!--: lemons = hello, hello -->
```

If `hello` contains `abc` then `lemons` will contain `abcabc`. However, if you also include a space string in between, like this...

```
<!-- lemons = hello, " ", hello -->
```

`lemons` will contain `abc abc`!

## errors
if there are error in this software plz report to me at https://github.com/ZoomTen/MDiocre/issues thanks!!
