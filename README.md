<img width="700" height="599" alt="image" src="https://github.com/user-attachments/assets/a1ae2ac6-09ad-401b-bce7-329027f08463" />

Create custom Maya menus for sharing tools with a team that can be automatically added to Maya's menu bar on launch. Menus can be updated/refreshed in-place when updates arrive without having to relaunch Maya. Using the optionBox next to each menuItem will add that action to your active Maya shelf.

After creating a menu using aMenuCreator, add it to the menuBar using:

<pre>from MenuCreator import menuFunctions
menuFunctions.createMenu('menuPathHere')</pre>

If you are wanting to have it load automatically everytime Maya is launched, create a userSetup.py file in your scripts folder and add:
<pre>import maya.cmds as mc
import maya.mel as mel

from MenuCreator import menuFunctions

mc.evalDeferred("menuFunctions.createMenu('menuPathHere')")</pre>

<img width="555" height="125" alt="image" src="https://github.com/user-attachments/assets/d472cab0-b33d-46b0-b0cf-b9a3e38fe4c2" />
