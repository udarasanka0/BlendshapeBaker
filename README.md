# BlendshapeBaker
A Maya tool for baking blendshape animations

# Blendshape Baker Tool 🏗️

A Maya tool for converting animation into blendshapes.

## 🛠️ How to Install

## Method 1 : Drag And Drop
1. Download `blendshape_baker.py` and `blendshapebaker.png`.
2. Drag and drop `blendshape_baker.py` into Maya's viewport.

## Method 2 : Install Permentaly
1. Download `blendshape_baker.py` and `blendshapebaker.png`.
2. Save it in your maya scripts folder
   Windows: C:\Users\YourUsername\Documents\maya\scripts\
   
4. Open the Script Editor, Switch to python and enter the following code
   
   import blendshape_baker
   
   blendshape_baker.show_ui()
   


   Select the text and middle-mouse drag it to a shelf (Custom, Animation, or a new shelf).

6. Right-click the new shelf button → Click Edit.
7. Change the icon if needed, and rename it (e.g., "Blendshape Baker").

   If you want the tool to be available every time Maya starts, follow these steps:

Open userSetup.py (or create it if missing) in the Maya scripts folder:

Windows: C:\Users\YourUsername\Documents\maya\scripts\userSetup.py

Add the following
import blendshape_baker


## 📌 Features
- Converts animations/Deformers/Alembic cache(Same topology)/Simulation effect  to blendshapes.
  - Works with any animated mesh.

## 📥 Download
[Click here to download](https://github.com/udarasanka0/BlendshapeBaker/archive/refs/heads/main.zip)
