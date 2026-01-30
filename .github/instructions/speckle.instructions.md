# Compare Versions

Source: https://docs.speckle.systems/3d-viewer/compare-versions

Compare two versions of a model to see the differences.

Speckle automatically tracks every change you make to your models. Each time you send data, a new [version](/workspaces/versions) is created. This allows you to review the entire history of your model, compare changes over time, and revert to earlier versions if needed.

## How It Works

Whenever you send data from a Speckle-enabled application (like Revit, Rhino, or Grasshopper), Speckle stores that data as a new version. Each version is:

-   Timestamped
-   Tagged with metadata (e.g. message, source application, sender)
-   Linked to previous versions, allowing for complete traceability and version comparison

Behind the scenes, Speckle breaks your model down into individual objects (such as walls, floors, meshes, or parameter sets) and gives each object a unique identifier.

<Note>Learn more about [versions here](/workspaces/versions).</Note>

### To compare two versions:

1. **Open the Models tab** on the left side of your screen.

2. **Click on the latest version** to expand the version list and view all available commits.

3. **Browse the list of commits** and identify the version you want to compare. Then click **_View Changes_** to see a detailed comparison.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/version-versions.jpg" />
</Frame>

<br />

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/version-comparison.jpg" />
</Frame>

## Benefits

-   **Change Awareness**: Understand how your model has evolved over time.
-   **Design Iteration**: Explore different design options across models without overwriting previous work.
-   **Collaboration**: See who made what changes and when, helping teams stay in sync.
-   **Recovery**: Roll back to a previous version if something goes wrong. <Warning>**Note**: Recovery is only supported in Rhino, Autocad and Sketchup connectors.</Warning>

## Tips

<Tip>
  * Use meaningful messages when sending data to make version tracking more readable.
  * Create models for separate project phases or design options to keep changes organized.
  * Use the diffing feature to compare versions and spot differences in geometry, parameters, or structure.
</Tip>

# Discussions

Source: https://docs.speckle.systems/3d-viewer/discussions

Leave comments and feedback exactly where it matters—in the 3D Viewer.

Discussions in Speckle are threaded conversations tied to specific objects or models, enabling teams to collaborate asynchronously and stay aligned without leaving the platform. They're ideal for reviewing models, giving feedback, and tracking decisions.

<Tip> **Tip:** Use Speckle's Discussions to keep all feedback tied to the actual model, reduce email threads, and speed up review cycles.</Tip>

## Communicate with Your Team

Add notes or questions to any object and chat live in the same panel. Attach comments to specific geometry for clear context,
see when teammates are typing, and reply instantly.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/discussions-side-panel.jpg" />
</Frame>

## Discussion Panel

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/comments-new.jpg" />
</Frame>

### Comments vs Discussions

While comments are quick, context-specific notes or reactions, discussions are structured threads meant for deeper conversations.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/comments.jpg" />
</Frame>

-   **Attach files**: Drag and drop images, PDFs, or other documents into threads to share references or detailed notes.

-   **Share a link** Generate a link to a comment or thread so teammates jump straight to the discussion in the model.

<Tip> Lock in a specific view and comment layout. Share the exact camera angle, view mode filters, and section cut so everyone sees the same snapshot.\
Try it yourself: [saved view](https://app.speckle.systems/projects/8be1007be1/models/5d98221bf2@f9948cdd8c#threadId=50cd9f8401)</Tip>

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/comments_share.jpg" />
</Frame>

### Resolving Discussions

Discussions can be resolved to indicate that a decision has been made or an issue has been addressed. Resolving helps declutter the interface and signals to other collaborators that no further input is required.

Only participants in the discussion or stream owners can resolve a discussion.

Resolved discussions are not deleted — they are hidden by default but can be shown at any time.

You can reopen resolved discussions if further input is needed.

### Hiding and Showing Past or Resolved Discussions

To keep the interface clean, Speckle allows you to:

-   Hide discussions related to past versions of the model or stream.

-   Show resolved discussions on demand to review decision history or context.

These visibility toggles can be accessed from the discussion panel filters, allowing you to focus only on what’s relevant.

### Mentions

Speckle supports **@mentions** in both comments and discussions. Mentioning a user:

-   Notifies them directly by email, drawing their attention to the discussion.

-   Helps delegate tasks or clarify responsibilities.

-   Ensures relevant stakeholders are kept in the loop.

To mention someone, type @ followed by their username. Suggestions will appear as you type.

### Best Practices

-   Use discussions for topics that require decisions, design debates, or extended feedback.

-   Keep comments short and context-specific.

-   Regularly resolve discussions to maintain focus.

-   Use @mentions to notify relevant collaborators and prevent delays.

# Exploration

Source: https://docs.speckle.systems/3d-viewer/exploration

The full hierarchy of your model is available for inspection and exploration.

## Scene Explorer

The Scene explorer is a panel that lets you navigate your 3D model using a familiar tree view:

1. **Hierarchy view:** See models organized by levels, categories, or custom groups.

2. **Visibility controls:** Show, hide, or isolate individual objects or groups with a single click.

Use the scene explorer to focus on the parts of your model you care about, cleanly
toggle layers, and understand the structure of complex scenes.

<Frame caption="Scene explorer">
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/scene_explorer.jpg" />
</Frame>

<Note>
  The model hierarchy displayed is as it is exported from the source application. There are some differences between each connector that
  reflects the typical workflows of users in that application.
</Note>

<AccordionGroup>
  <Accordion title="Can I show the hierarchy in a different order?">
    No, the hierarchy is as it is exported from the source application. Our developer documentation has more information on how to work with the underlying data that could achieve this.
  </Accordion>
</AccordionGroup>

### Dev(eloper) Mode

Dev mode gives you a deeper look into your model's data structure:

-   **Full hierarchy view.** See every object, list, and parameter exactly as Speckle stores it.

-   **Raw JSON inspection.** View and copy the underlying JSON data for any item; perfect for developers or power users.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/dev_mode.jpg" />
</Frame>

<Tip>Use Dev mode when you need complete transparency or want to integrate Speckle data into your own workflows and applications.</Tip>

<AccordionGroup>
  <Accordion title="How do I enable Dev mode?">
    Dev mode is enabled by default for all Speckle users.
  </Accordion>

  <Accordion title="How do see the data for a single object?">
    Click on an object in the hierarchy view to see the data for that object above the overall hierarchy view.
  </Accordion>

  <Accordion title="Can I see the raw JSON data for a property?">
    Dev mode visualises the JSON structure. Our developer docs have more information on how to access and use the raw data view.
  </Accordion>
</AccordionGroup>

## Filtering by Property Data

Speckle's filtering tools let you quickly find, highlight, and analyze parts of your
model based on any property or parameter:

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/filtering.jpg" />
</Frame>

Filter and search:

1. Open the filter panel and choose any property from your model (e.g., category,
   level, tag).

2. Type or select values to narrow down the list of objects.

3. Click the brush icon on the top right corner of the panel to color-code the model.

4. Query specific values. Use the search box to look for a particular value within
   the filtered property (e.g., all "category" Walls with “FireRating = 2”).

<Tip>**Tip:** First, use a filter in combination with isolate, then apply another
filter to explore the model further.</Tip>

<AccordionGroup>
  <Accordion title="How do I filter by a custom property?">
    Any property in the model can be filtered on.
  </Accordion>

  <Accordion title="Can I filter by a property that doesn't exist?">
    No, the property must exist in the model. However you could use the Model Checker premade automation to add a test for a property and its results can be used as a filter.
  </Accordion>

  <Accordion title="How can I know what properties are available?">
    As you type in either the property search bar or the value search bar, Speckle will show a list of properties that match the text you've typed.
  </Accordion>
</AccordionGroup>

## Measure Mode

Use the Measure tool to verify dimensions, check clearances, and validate design details without leaving the viewer.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/measure_mode.jpg" />
</Frame>

### Measurement Types

-   **Point-to-point measurement.** Click two points in the model to get the straight-line distance.
-   **Perpendicular measurement.** Measure the shortest distance from a point to a line or plane.
-   **Area measurement.** Measure the area of a polygon or closed polyline.
-   **Point coordinates.** Get the exact XYZ coordinates at any point in the model.

### Measurment Settings

-   **Snap to vertices**: Toggle snapping to the nearest vertex on the model.
-   **Chain measurements**: Toggle chaining measurements for point-to-point measurements.
-   **Units**: Switch to your preferred unit display from standard length units (mm, m, ft, in) in imperial or metric.
-   **Precision**: Adjust the decimal precision to suit your needs.
-   **Delete measurements**: Delete all measurements from the model.

<AccordionGroup>
  <Accordion title="How do I cancel a measurement?">
    Press the `Escape` key on your keyboard to stop chaining measurment points, or conclude the area measurement.
  </Accordion>

  <Accordion title="Can I measure the area of a slope?">
    Yes, your first measurement point will be both a start point and also define the plane of the area measurement.
  </Accordion>

  <Accordion title="Can I add multiple areas to gain a sum total?">
    No, Each area measurement is it's own entity. For more complex area measurements you can add the Room and Area Scheduler premade automation to your model.
  </Accordion>
</AccordionGroup>

# Model Federation

Source: https://docs.speckle.systems/3d-viewer/federation

Assemble models from different software into one cohesive view.

Model federation makes it easy for different teams, like architects, structural engineers,
and MEP designers, to share and combine their models without sending huge files back and forth.

Speckle lets you combine models created in different software, Revit, Rhino, AutoCAD, and more,
without juggling huge files.

## How does it work?

1. **Publish separately.**
   Each team uploads their model straight from the tool they use into a Speckle project
   (think a project folder that holds all the models).

2. **Assemble on demand.**
   In your project, click Add in the left sidebar to bring in other models alongside
   the one you opened.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/model_fed.jpg" />
</Frame>

3. **Combine everything.**
   From the main project view, click View All in 3D. This opens the 3D Viewer and
   displays every model together in one scene.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/federation_all.jpg" />
</Frame>

<Note>When a federated model view is generated from the a model folder, additional project models can be added to the federation,
but none removed from the view. Instead either assemble a federation by adding models one at a time, or use the hide and isolation tools.</Note>

# Interface and Navigation

Source: https://docs.speckle.systems/3d-viewer/interface-nav

Finding your way around the 3D viewer and the tools available to you.

The Speckle model viewer allows you to explore your 3D models directly in your browser. Below is a guide to help you
understand the interface and how to interact with your model.

## Overview

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/navigation_overview.jpg" />
</Frame>

### Top Navigation

-   **Workspace (top-left):**\
    Displays your current workspace.\
    Click to switch to a different one or access workspace settings:

-   **Navigation (top-center):**\
    Shows your location in Speckle:\
    **All Projects → Project → Model**

-   **Share button (top-right):**\
    Click to share the model via link or manage access permissions.

-   **User avatar (top-right corner):**\
    Access your account settings or sign out.

### Toolbar (left sidebar)

From top to bottom:

1. **Models**: Manage model versions and add or remove models from the scene.
2. **Scene explorer**: Explore your model's data and apply filters.
3. **Discussions**: View and participate in comments and discussions within the model.
4. **Measure**: Take quick measurements directly in the 3D view.
5. **View modes**: Switch between different visual styles (e.g., Pen, Arctic, Shaded).
6. **Views**: Change camera angles (e.g., Top, Front, Side).
7. **Fit**: Automatically center and fit the model to your screen.
8. **Light controls**: Adjust lighting settings to improve visibility and contrast.
9. **Projection**: Toggle between perspective and orthographic camera views.
10. **Section**: Use the section box to slice through the model and inspect interior geometry.
11. **Explode model**: Explode components of the model to better understand its structure.
12. **Free orbit**: Allows full 360° orbiting around and beneath the model.

## Selection Info Panel (right sidebar)

Speckle is a platform designed to streamline data exchange and collaboration in the architecture, engineering, and construction
(AEC) industries. It connects various design and modeling software—such as Revit, Rhino, Grasshopper, AutoCAD, and others—and
enables the extraction of detailed object properties from each.

Each software plugin in Speckle translates native objects (like walls, beams, or curves) into a standardized Speckle format.
During this process, key properties—such as geometry, materials, dimensions, and metadata—are captured and stored in Speckle.
These properties remain intact and are accessible regardless of the originating software.

Once extracted, Speckle allows users to visualize and explore these objects and their properties in a web-based 3D viewer
using the **Selection info panel**.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/sel_info_panel.jpg" />
</Frame>

### Visibility Controls

With an object or objects selected, you can control their visibility or isolation from the rest of the model using the following buttons.

-   **Hide and isolate controls:**\
    Located at the top-left of the panel:

    -   **Hide**: Temporarily removes selected object(s) from view.
    -   **Isolate**: Hides everything except the selected object(s).

-   **Open object in a new window:**\
    Located at the top-right corner of the panel:
    -   Clicking this button opens a new window focused solely on the selected object. This is an excellent way to isolate
        and explore unique objects in greater detail or to share them with external collaborators for inspection.

### Object Properties

All objects have a set of properties that are used to describe them. These properties are extracted from the original software
and stored in Speckle. How many properties are available depends on the host application. The object properties panel provides
detailed information about any object selected within your Speckle model. This metadata is essential for understanding the
object's characteristics and for making informed decisions during collaboration and analysis.

When you select an object, this panel will display key attributes, including but not limited to:

-   **id**, **name**, **volume**, **type**, and more

<Note>The exact properties shown depend on the host application from which the data was extracted. In the legacy connectors, each
software captures and structured object data differently, in the current connectors efforts have been made such that while the
available attributes may vary, the structure is more consistent. Extremely useful for automation and data analysis.</Note>

# Presentation

Source: https://docs.speckle.systems/3d-viewer/presentation

View your 3D Model anywhere

## View Modes

Use view modes to find the perfect visual setup for presenting, reviewing, or working on your model.

<Frame caption="The different appearance of the available view modes">
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/view_modes_2.jpg" />
</Frame>

### View Mode Settings

Speckle's view modes let you switch visual styles and tweak display settings to suit your needs:

-   **Pick a style.** Pick from Pen, Arctic, Shaded and more styles.
-   **Edge toggle.** Turn edge lines on or off to highlight or simplify your view.
-   **Line thickness.** Easily make lines thicker or thinner for clearer outlines and emphasis.
-   **Change color.** Change the color of the model outlines to match your presentation or for clarity.

<Frame caption="Select and configure the view modes">
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/view_mode.jpg" />
</Frame>

<AccordionGroup>
  <Accordion title="Can I set a default view mode?">
    No, the view mode is set on a view by view basis at view time. You can lock in a view mode by creating a comment and all viewer settings are locked in if you review that comment.
  </Accordion>

  <Accordion title="Can I set the edges to always be off?">
    No, edges start on by default.
  </Accordion>

  <Accordion title="Can I set the line thickness to always be a certain value related to the model scale?">
    No, the line thickness is a setting relative the view. As you zoom in and out the line thickness will maintain a consistent size.
  </Accordion>

  <Accordion title="I have a very detailed model, will the edges be visible?">
    There is some clever rendering going on to ensure that edges are visible even on very detailed models without becoming too busy.
  </Accordion>
</AccordionGroup>

## Section

The Section box lets you carve out a 3D region in your model to reveal and inspect its interior geometry.
Simply position and resize the box to slice through walls, floors, or any elements, exposing hidden details for
review or presentation without permanently altering your model.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/section.jpg" />
</Frame>

The section tool can be used to create unique views of the model for presentations or design review. You can control:

-   **Position**: Use the translation gizmo at the center of the section box to move in the direction of each axis.
-   **Rotation**: Use the rotation gizmo at the center of the section box to rotate in the direction of each axis.
-   **Size**: Select a virtual face of the section box and then use the translation gizmo at the center of the face to move
    it in the perpendicular direction.

<AccordionGroup>
  <Accordion title="Can I set a default section?">
    No, the section tool defaults to a 3D region encompassing the bounding box of the model or selected elements. You can lock in a section by creating a comment and all viewer settings are locked in if you review that comment.
  </Accordion>

  <Accordion title="Can I set individual section planes?">
    No, the section tool defaults to a single cuboid region encompassing the bounding box of the model or selected elements.
  </Accordion>

  <Accordion title="Can I set multiple section boxes?">
    No, the section tool defaults to a single cuboid region encompassing the bounding box of the model or selected elements.
  </Accordion>
</AccordionGroup>

## Lighting Controls

Use Light Controls to make sure every part of your model is clearly visible, whether you're inspecting fine details or presenting to stakeholders.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/light_controls.jpg" />
</Frame>

### Light Controls Settings

Speckle's lighting controls let you tweak how your model is lit to improve visibility and contrast:

-   **Intensity.** Increase or decrease overall brightness to suit your environment.

-   **Elevation.** Adjust the vertical angle of the light source to highlight different surfaces.

-   **Azimuth.** Change the horizontal rotation of the light to control shadow direction.

-   **Indirect.** Modify the amount of ambient or bounced light for softer, more realistic shading.

<AccordionGroup>
  <Accordion title="Can I set a default light control?">
    No, the light control is set on a view by view basis at view time. You can lock in a light control by creating a comment and all viewer settings are locked in if you review that comment.
  </Accordion>

  <Accordion title="Can I set the lighting to be a real time of day?">
    No, the lighting is quasi-real-world relative to model space.
  </Accordion>

  <Accordion title="Can I specify a location in the world for the lighting?">
    No, the lighting is relative to the model space and doesn't have a world location.
  </Accordion>

  <Accordion title="Can I export the shadows?">
    No, the shadows are only visible in the viewer.
  </Accordion>
</AccordionGroup>

## Explode

The Explode tool breaks your model into its individual components, spreading them apart in the 3D space. This works best for small details or products to understand how they come together.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/explode.jpg" />
</Frame>

<Note>The elements that are exploding are determined by the source data from the host application.
i.e. If an element is aggregated as a composite in one object, it may not explode into its components.</Note>

<AccordionGroup>
  <Accordion title="Can I constrain the explode to a single axis?">
    No, the explode is radial from the center of the model.
  </Accordion>

  <Accordion title="Can I explode by floor or other model elements?">
    No the explode is only available for the model as a whole.
  </Accordion>

  <Accordion title="Can I explode a section?">
    Yes, you can explode the model while a section is active.
  </Accordion>

  <Accordion title="Why do some parts of the model explode more than others?">
    The explode is a radial operation from the center of the model. Elements that are closer to the center of the model explode more than elements that are further away.
  </Accordion>
</AccordionGroup>

## Canonical Views

You can set the camera position and view to a canonical view: Top, Front, Left, Right, and Back.

<AccordionGroup>
  <Accordion title="Can I set a default canonical view?">
    No, the canonical view defaults to a perspective top down from left to right. You can lock in a canonical view by creating a comment and all viewer settings are locked in if you review that comment.
  </Accordion>

  <Accordion title="Can I set additional canonical views?">
    No, the canonical views are predefined. Connectors may publish additional views that will be displayed in the canonical views dropdown.
  </Accordion>

  <Accordion title="Can I add 2d plan or section drawings to include in the view?">
    No, the canonical views are 3d views of model data. 2D data may be included in the models sent to Speckle, but not added to the canonical views.
  </Accordion>

  <Accordion title="Can I show the levels/grids of the model in the view?">
    No, the canonical views are 3d views of model data. Levels, grids, and other 2d data may be included in the models sent to Speckle, but not added to the canonical views.
  </Accordion>
</AccordionGroup>

## Projection

Speckle's Projection settings let you switch between different camera views:

-   **Perspective.** A realistic view with vanishing points, perfect for presentations and spatial understanding.

-   **Orthographic.** A flat, scale-accurate view without perspective distortion, ideal for precise measurement and technical review.

<AccordionGroup>
  <Accordion title="Can I set a default projection?">
    No, the projection defaults to perspective. You can lock in a projection by creating a comment and all viewer settings are locked in if you review that comment.
  </Accordion>

  <Accordion title="Can I change the FOV of the perspective view?">
    No, the fov and aspect ratio are fixed. It is approximately equivalent to a 50mm lens on a full frame camera.
  </Accordion>
</AccordionGroup>

## Fit

The Fit tool adjusts the camera to fit the entire model in the view. If an object or objects are selected, the Fit tool will fit the camera to the selected objects.

# Share your Models

Source: https://docs.speckle.systems/3d-viewer/sharing

View your 3D Model anywhere

## Share Using a URL link

With Speckle, sharing your 3D models is as easy as copying a link or embedding an interactive viewer—no huge file
transfers required. Because Speckle is a web app, you can access and interact with your models from any device—desktop,
tablet, or phone—from anywhere with an internet connection. **No special software or licenses are required to view and
interact with models;** everything runs right in your browser:

You have two simple ways to share your Speckle model:

1. **Copy and paste the URL**\
   Just grab the link from your browser's address bar and send it to anyone who needs access.

2. **Use the Share button**\
   Click Share in the top-right corner, then select Copy link. Paste that link wherever you like.

<Frame caption="Share your model using the URL link">
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/share_url_link.jpg" />
</Frame>

<Warning>
  If someone can't open your link, check your project's permissions. You may need to give them access to your workspace or
  project first. For details, see [Managing Access and Permissions](/workspace-setup/workspaces#managing-access-and-permissions) guide.
</Warning>

## Embed the 3D Viewer

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/embed_1.jpg" />
</Frame>

### Options and settings

-   **Embed code** (iframe)
-   **Embed URL**
    Use the direct viewer URL if you need a quick link to open the model in a new browser tab without embedding code.
-   **Options and Preview**
    Customize and toggle the following: Transparent background, Hide viewer controls, Hide the selection info panel, Prevent scrolling (zooming), Load model manually.

<Frame caption="Embed your model using the iframe code">
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/3d-viewer/embed_options.jpg" />
</Frame>

## Examples

### Speckle in Miro

<div style={{ position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden' }}>
  <iframe
    src="https://player.vimeo.com/video/1087137665"
    allowFullScreen
    loading="lazy"
    style={{
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
  }}
  />
</div>

### Speckle in Notion

<div style={{ position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden' }}>
  <iframe
    src="https://player.vimeo.com/video/1087045865"
    allowFullScreen
    loading="lazy"
    style={{
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
  }}
  />
</div>

# How to use Speckle for Archicad

Source: https://docs.speckle.systems/connectors/archicad

Step-by-step guide for using the Archicad connector

export const app_4 = "Archicad"

export const app_3 = "Archicad"

export const app_2 = "Archicad"

export const app_1 = "Archicad"

export const app_0 = "Archicad"

export const versions_0 = "27 & 28"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Archicad connector">
    1. In Archicad, select **Speckle** from the menu.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/archicad_toolbar.jpg" alt="Archicad toolbar" />
    </Frame>

    2. Select **Speckle** to open the Archicad connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What is addon registration? What can I do if it fails?">
    If the Speckle addon doesn't appear in Archicad's Add-On Manager, or if a warning icon appears next to it, try unloading the addon and then loading it manually. You can refer to the [Archicad Add-On Manager Help](https://claude.ai/chat/link-needed) for assistance.

    If the connector installation was successful, you can find the addon file at:

    * **Archicad 28**: `C:\Users\{username}\AppData\Roaming\Speckle\Archicad\v3\28\Add-Ons\Speckle.apx`
    * **Archicad 27**: `C:\Users\{username}\AppData\Roaming\Speckle\Archicad\v3\27\Add-Ons\Speckle.apx`

  </Accordion>

  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of Archicad elements can I publish to Speckle?">
    You can publish all 3D elements that include a mesh, including:

    * `Wall`, `slab`, `beam`, `column`
    * `Door`, `window`, `curtain wall`, `skylight`, `object`
    * `Roof`, `shell`, `morph`, `mesh`
    * `Stair`, `railing`

    <Note> Elements that aren't visible in the 3D view won't be published. </Note>

  </Accordion>

  <Accordion title="How do I publish models from Archicad views?">
    1. Set the **Filter** setting to **Views** while publishing a new version to your Speckle model.
    2. Select the view you want to publish from.
  </Accordion>

  <Accordion title="How do I publish models by Archicad element type?">
    1. Set the **Filter** setting to **Element Types** while publishing a new version to your Speckle model.
    2. Select the element types you want to publish.
  </Accordion>

  <Accordion title="How do I see custom properties on my published Archicad elements?">
    All custom properties appear under the properties field when you select and view an Archicad object in your browser. Custom properties vary depending on the type of Archicad element, and can include:

    * Element ID, element type, element name, level
    * Classifications
    * Dimensional properties
    * Material quantities
    * User-defined properties
    * IFC properties

    <Note> For IFC properties, the property mapping of the default IFC translator determines what gets exported.</Note>

  </Accordion>

  <Accordion title="Publishing my model takes a long time. Can I speed it up?">
    Yes. If element properties aren't required, you can disable property extraction to speed up the publishing process.
    **To disable property extraction**

    1. Open the **Send Settings**.
    2. Turn off the **Include Object Properties** option.
       <Note> Disabling property extraction can significantly reduce publish time. </Note>

  </Accordion>

  <Accordion title="What doesn't get published with the Archicad connector?">
    The following items don't get published:

    * 2D documentation: floor plans, sections, elevations
    * 2D elements: lines, hatches, dimensions
    * Surface textures

  </Accordion>

  <Accordion title="Which element properties aren't published with the Archicad connector?">
    Some built-in properties under **Element Properties** > **Dimensional Properties** aren't published. This optimization improves publishing speed and avoids redundancy in the published data.
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Select Load">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_1.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_2.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a model">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_3.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a version to load">
    * Latest version is always first.
    * To load a specific version, select it from the UI.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_4.jpg" alt="Load" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_5.jpg" alt="Load" />
    </Frame>

    Your selected model is now loaded in {app_3}.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How are Speckle models loaded in Archicad?">
    All objects in Speckle models are loaded as GDL objects (generic models) in Archicad. If your model contains block instances, each instance will be loaded as its own generic model. Each object will be loaded with:

    * Render material (if any)
    * Mesh geometry

    <Note> The loaded GDL objects are organized in folders in Archicad's embedded library. The folder name is: ´Project Name - Model Name´ </Note>

  </Accordion>

  <Accordion title="How are the loaded GDL objects displayed on floor plan views in Archicad?">
    Currently, the 2D script of the GDL object generates only cut lines at the floor plan cut plane on each level. Projection lines aren't shown.
  </Accordion>

  <Accordion title="Can I load custom properties in Archicad?">
    Currently, you can't load any custom properties on your Speckle model objects into Archicad.
  </Accordion>

  <Accordion title="Why was my Speckle model was loaded in an incorrect position?">
    If you're loading models published from Revit, ask the author of the model to publish again using the correct reference point from their Revit file.
    For models from other applications, please request a reference coordination feature in our [Community Forum](https://speckle.community/c/features).
  </Accordion>

  <Accordion title="Why are some objects that I loaded missing from my model?">
    After you load a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for loading in {app_4}.
  </Accordion>

  <Accordion title="Why can't I select a project in the UI—it's disabled?">
    This happens when you don't have permissions to load a project. Contact the project owner to change your role.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Next to the search box in the project selection dialog, there's an **Add model by URL** option. Paste the model URL there.
  </Accordion>
</AccordionGroup>

# How to use Speckle for AutoCAD

Source: https://docs.speckle.systems/connectors/autocad

Step-by-step guide for using the AutoCAD connector

export const app_4 = "AutoCAD"

export const app_3 = "AutoCAD"

export const app_2 = "AutoCAD"

export const app_1 = "AutoCAD"

export const app_0 = "AutoCAD"

export const versions_0 = "2022, 2023, 2024, 2025, & 2026"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the AutoCAD connector">
    1. In AutoCAD, select the **Speckle** tab in the ribbon.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/autocad_toolbar.jpg" alt="AutoCAD toolbar" />
    </Frame>

    2. Select **Speckle** to open the AutoCAD connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of AutoCAD elements can I publish to Speckle?">
    All types of `Geometry` can be published, as well as `Hatch`, `Text`, and `Blocks`. Each published object contains the following information:

    * Color
    * Render material

  </Accordion>

  <Accordion title="Can I publish solids from AutoCAD?">
    Solids will only be published as `Mesh` geometry.
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Select Load">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_1.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_2.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a model">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_3.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a version to load">
    * Latest version is always first.
    * To load a specific version, select it from the UI.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_4.jpg" alt="Load" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_5.jpg" alt="Load" />
    </Frame>

    Your selected model is now loaded in {app_3}.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How are Speckle models loaded in AutoCAD?">
    All objects in Speckle models are loaded as `geometry`, `text`, or `blocks` in AutoCAD. They will be created in a flattened layer structure as what you see when viewing your model in your browser. Each object will be loaded with:

    * Render material (if any)
    * Color (if any)

  </Accordion>

  <Accordion title="How do I select all the layers created after loading a Speckle Model?">
    Speckle models are loaded into their own `Selection Set`. You can use this to easily select all layers created by your loaded model.
  </Accordion>

  <Accordion title="Why are some objects that I loaded missing from my model?">
    After you load a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for loading in {app_4}.
  </Accordion>

  <Accordion title="Why can't I select a project in the UI—it's disabled?">
    This happens when you don't have permissions to load a project. Contact the project owner to change your role.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Next to the search box in the project selection dialog, there's an **Add model by URL** option. Paste the model URL there.
  </Accordion>
</AccordionGroup>

# How to use Speckle for Blender (beta)

Source: https://docs.speckle.systems/connectors/blender

Step-by-step guide for using the Blender (beta) connector

export const app_3 = "Blender"

export const app_2 = "Blender"

export const app_1 = "Blender"

export const app_0 = "Blender"

export const versions_0 = "4.2, 4.3, 4.4, & 4.5"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Tip>
  {' '}

Blender is currently in **beta**. There may be bugs while the connector is still
in development.
</Tip>

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Blender connector">
    1. Press **N** from your keyboard to open the side toolbar.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/blender_toolbar.jpg" alt="Blender toolbar" />
    </Frame>

    2. Select **Speckle** to open the Blender connector.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why don't I see Speckle in the side toolbar?">
    Make sure you activated the Speckle connector:

    1. Go to **Edit** > **Preferences** > **Add-ons**
    2. Search for **Speckle**
    3. Select **Install**

  </Accordion>

  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish" />

{' '}

  <Step title="Choose a project" />

{' '}

  <Step title="Choose a model" />

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.
    3. Your model is now published to Speckle and is available to the rest of your team.
  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of objects are published?">
    All types of `Mesh`, `Bezier`, `Circle`, `NURBS Curve` and `NURBS Circle` are supported.

    <Warning>`Camera` and `Lights` are not supported.</Warning>

  </Accordion>

  <Accordion title="Why don't materials look correct in the viewer?">
    Blender connector only supports the following shaders:

    * Principled
    * Diffuse
    * Emission
    * Glass

    Blender will fallback to material properties if an unsupported shader is selected.

  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Select Load" />

{' '}

  <Step title="Choose a project" />

{' '}

  <Step title="Choose a model" />

  <Step title="Choose a version to load">
    * Latest version is loaded by default.
    * To load a specific version, select it from the UI.
      Your selected model is now loaded in Blender.
  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="After I load a model, can I make changes to loaded elements and will they be preserved when I load a new version?">
    You can modify **materials** and it will be preserved when you load a new version.
  </Accordion>

  <Accordion title="Where are my properties?">
    Currently, properties are **not** loaded and attached to loaded objects.
  </Accordion>

  <Accordion title="How are my blocks loaded in Blender?">
    Blocks are loaded as collection instances.
  </Accordion>

  <Accordion title="Why are some objects that I loaded missing from my model?">
    After you load a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for loading in {app_3}.
  </Accordion>

  <Accordion title="Why can't I select a project in the UI—it's disabled?">
    This happens when you don't have permissions to load a project. Contact the project owner to change your role.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Next to the search box in the project selection dialog, there's an **Add model by URL** option. Paste the model URL there.
  </Accordion>
</AccordionGroup>

# How to use Speckle for Civil 3D

Source: https://docs.speckle.systems/connectors/civil3d

Step-by-step guide for using the Civil 3D connector

export const app_4 = "Civil 3D"

export const app_3 = "Civil 3D"

export const app_2 = "Civil 3D"

export const app_1 = "Civil 3D"

export const app_0 = "Civil 3D"

export const versions_0 = "2022, 2023, 2024, 2025, & 2026"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Civil 3D connector">
    1. In Civil 3D, select the **Speckle** tab in the ribbon.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/civil_toolbar.jpg" alt="Civil 3D toolbar" />
    </Frame>

    2. Select **Speckle** to open the Civil 3D connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of Civil 3D elements can I publish to Speckle?">
    All visible types of objects supported by AutoCAD can be published from Civil 3D: `Geometry` , `Hatch`, `Text`, and `Blocks`. In addition to AutoCAD elements, any civil entity can be published as a `CivilObject`  as well, and will contain:

    * type
    * base curve (if any)
    * children elements (e.g. corridor baselines)
    * custom properties
    * color
    * render material

  </Accordion>

  <Accordion title="Can I publish solids from Civil 3D?">
    Solids will only be published as `Mesh` geometry.
  </Accordion>

  <Accordion title="How do I see the custom properties on my published Civil 3D elements?">
    All custom properties can be found under the `properties` field when you select and view a Civil 3D object in your browser.Custom properties vary depending on the type of civil element, and can include:

    * extension dictionary
    * property set
    * Network part: part data
    * Catchment: hydrological and hydraulic props
    * Surface: statistics
    * Corridor: featurelines and codes
    * and more

  </Accordion>

  <Accordion title="How do I make sure my Civil 3D model is aligned with my other Speckle models?">
    Currently, there is no option to publish your model from a specific reference point. If you would a reference point setting for Civil 3D, please request the reference coordination feature in our Community Forum: [https://speckle.community/c/features](https://speckle.community/c/features)
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Select Load">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_1.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_2.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a model">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_3.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a version to load">
    * Latest version is always first.
    * To load a specific version, select it from the UI.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_4.jpg" alt="Load" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_5.jpg" alt="Load" />
    </Frame>

    Your selected model is now loaded in {app_3}.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How are Speckle models loaded in Civil 3D?">
    All objects in Speckle models are loaded as `geometry`, `text`, or `blocks` in Civil 3D. They will be created in a flattened layer structure as what you see when viewing your model in your browser. Each object will be loaded with:

    * render material (if any)
    * color (if any)

  </Accordion>

  <Accordion title="How do I select all the layers created after loading a Speckle Model?">
    Speckle models are loaded into their own `Selection Set`. You can use this to easily select all layers created by your loaded model.
  </Accordion>

  <Accordion title="Why are some objects that I loaded missing from my model?">
    After you load a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for loading in {app_4}.
  </Accordion>

  <Accordion title="Why can't I select a project in the UI—it's disabled?">
    This happens when you don't have permissions to load a project. Contact the project owner to change your role.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Next to the search box in the project selection dialog, there's an **Add model by URL** option. Paste the model URL there.
  </Accordion>
</AccordionGroup>

# IFC and File Imports

Source: https://docs.speckle.systems/connectors/direct-uploads/file-uploads

How to upload files directly to Speckle

export const app_0 = "IFC"

export const versions_0 = "IFC2x3, IFC4 & IFC4x3"

export const os_0 = undefined

<Info>
  Supported file formats: **IFC, STL & OBJ**.
</Info>

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

Our file import feature makes it easy for you to drag and drop files directly into your Speckle project.
Use the **file import** method when:

-   you want IFC data in Speckle format
-   there is no Speckle connector available for your app
-   you can't or don't want to open a desktop software to view a model in your browser
-   you have a file from a collaborator who isn't using Speckle.

<Note>IFC and file uploads is a beta functionality currently in development</Note>

### Getting Started

<Steps>
  <Step title="Create a new project">
    You will see a prompt to upload a file or publish from a connector.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/files/file-upload.png" alt="upload" />
    </Frame>

  </Step>

  <Step title="Drag and drop your file">
    Drag and drop the file on the project to initiate the upload, a new model will be created with the file name.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/files/file-uploading.png" alt="uploading" />
    </Frame>

  </Step>

  <Step title="Upload new versions">
    Use the dropdown menu on the model to upload new versions.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/files/file-new_version.png" alt="new version" />
    </Frame>

  </Step>
</Steps>

### General FAQ

<Note>Please note, file downloads are currently not possible.</Note>

<AccordionGroup>
  <Accordion title="Will you support other formats for direct upload?">
    We are currently limited to open-source formats because of licensing restrictions. If there are other formats you would like to see supported, please let us know.
  </Accordion>

  <Accordion title="My file is too large to upload">
    The limits on file uploads are currently 100MB for all plans and all formats.
  </Accordion>

  <Accordion title="I have uploaded a file but it's not visible or still processing.">
    We use a queue system to process files, so it can take awhile to generate the Speckle model after you upload your file.
    If you do not see your model after a long time, this may be caused by faulty items inside your file.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your file type and version (if applicable)
    * Your failed file (if possible)

  </Accordion>
</AccordionGroup>

### IFC FAQ

<AccordionGroup>
  <Accordion title="Will you support IFC versions other than IFC2x3, IFC4 & IFC4x3?">
    We currently support whatever formats the [web-ifc project](https://thatopen.github.io/engine_web-ifc/docs/) supports which Speckle uses under the hood.
  </Accordion>

  <Accordion title="Why are some objects missing in my IFC file?">
    Some types are not supported either in part or entirely, including:

    * IfcSpace (no geometry)
    * IfcSite (no geometry)
    * IfcAnnotation

  </Accordion>

  <Accordion title="Are objects uploaded with their class properties?">
    No, currently IFC uploaded objects do not include class properties.
  </Accordion>

  <Accordion title="Why are the units different in my uploaded IFC model?">
    To handle unit compatibility with other Speckle models, all uploaded IFC models are converted to meters.
  </Accordion>
</AccordionGroup>

# How to use Speckle for ETABS

Source: https://docs.speckle.systems/connectors/etabs

Step-by-step guide for using the ETABS connector

export const app_3 = "ETABS"

export const app_2 = "ETABS"

export const app_1 = "ETABS"

export const app_0 = "ETABS"

export const versions_0 = "21 & 22"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the ETABS connector">
    1. Go to **Tools**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/etabs_toolbar.jpg" alt="ETABS toolbar" />
    </Frame>

    2. Select **Speckle** to open the ETABS connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How do I manually load the connector?">
    If the plugin is not showing up under Tools, you can manually load the ETABS connector:

    1. Navigate to `Tools -> Add/Show Plugins...`
    2. Click `Browse` and navigate to the path `{localappdata}\Computers and Structures\ETABS xx\Speckle\`
    3. Select the `SpeckleConnectorCSI.dll` file. Click `Add` and then `Ok`.

  </Accordion>

  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of ETABS elements can I publish to Speckle?">
    All selectable model objects can be published: `Joints`, `Frames`, `Tendons`, `Shells` and `Links`. Each published object contains the following information:

    * Type
    * Geometry as `Mesh` , `Curve` or `Point`
    * Children objects, such as `Joints`
    * Custom properties

  </Accordion>

  <Accordion title="How do I see the custom properties on my published ETABS elements, like sections or area metrics?">
    All custom properties can be found under the `properties` field when you select and view an ETABS object in your browser.Custom properties vary depending on the type of ETABS element, and can include:

    * Assignments (e.g. `material` and `section`)
    * Geometry metrics (e.g. length or area)
    * Object ID (e.g. sub-classification for `Frame` -> `Column`, `Beam`, or `Brace` , label, and associated level)

  </Accordion>

  <Accordion title="Where can I find the material or section used for an object in my Speckle model?">
    The specific properties for materials and sections will not appear on individual model objects. To view your model materials and sections in your web browser:

    1. Open the `Scene Explorer` tab in the Navigation Bar to the left (or press `Shift` + `E`)
    2. Click `Switch to Dev Mode`. This will give you full access to all objects and properties in your model.
    3. Expand the `sectionProxies` or `materialProxies` item.
    4. Expand any item in this list to see a `Section` or `Material` with all of its properties.The section can be matched back to any element based on its `name`, and the material can be matched to any section based on its `name`.

  </Accordion>

  <Accordion title="Which object properties do not get published with the ETABS connector?">
    Currently\*\*,\*\* the following properties are *not* published on objects:

    * Load cases, patterns and combinations
    * Analysis results
    * Grids and grid information
    * Levels information

  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Note>The {app_3} connector is publish-only.</Note>
If you would like to be able to load a model into {app_3}, please reach out on our Community Forum: [https://speckle.community/c/features](https://speckle.community/c/features/7)
Include the following information:

-   Which application your Speckle model is published from
-   Why you want to load your model into {app_3}
-   How frequently you would use this workflow (daily, weekly, monthly, longer).

# How to use Speckle for Grasshopper (alpha)

Source: https://docs.speckle.systems/connectors/grasshopper

Step-by-step guide for using the Grasshopper (alpha) connector

export const app_2 = "Grasshopper"

export const app_1 = "Grasshopper"

export const app_0 = "Grasshopper"

export const versions_0 = "Rhino 7 & 8"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Tip> The **Rhino** and **Grasshopper** connectors are bundled, so if you installed one, you don't need to install the other.</Tip>
<Tip> Grasshopper is currently in **alpha**. There may be bugs while the connector is still in development.</Tip>

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Grasshopper connector">
    1. In Rhino, add your account in the Rhino connector.
    2. Open Grasshopper, and select the **Speckle** tab in the ribbon.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/grasshopper_toolbar.jpg" alt="Grasshopper toolbar" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Tip>
  Full documentation of all Grasshopper nodes and sample scripts are installed with your connector.
  Navigate to **File** > **Special Folders** > **Components Folder** > **Speckle Sample Files** in Grasshopper to find them.
</Tip>

<Steps>
  <Step title="Create a Collection with objects">
    1. Add a **Create Collection** node from the `Collections` category to the canvas.
    2. Connect the geometry you want to publish to the input of the **Create Collection** node.
  </Step>

  <Step title="Get your Speckle model link">
    1. Add a **Speckle Model URL** node to the canvas.
    2. Choose a project:
       * Click on the **Project** button to select a project from the dropdown
       * or use the search bar to find another project.
    3. Choose a model:
       * Click on the **Model** button to select a model from the dropdown
       * or use the search bar to find another model.
  </Step>

  <Step title="Publish your model">
    1. Add a **Publish** node to the canvas and connect your inputs:

    * Add your **Create Collection** output to the Collection input.
    * Add your **Speckle Model URL** output to the Model Link input.

    2. Click **Publish**.
       Your model is now published to Speckle and is available to the rest of your team.

    <Frame title="Publish">
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/grasshopper_publish.jpg" alt="Grasshopper publish" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How do I create properties by key value, instead of using the Create Properties node?">
    In Rhino 8, you can use the native Grasshopper **User Text** node to create properties by keys and values.
    Just plug the Content output of the node into any input expecting a Speckle Properties param.
    In Rhino 7, currently there is no way to create properties by key value.
  </Accordion>

  <Accordion title="How do I sync my property and collection names with their inputs?">
    If you keep your params organized with their own names, then you can easily inherit these names when using the **Create Properties** or **Create Collection** nodes.
    To sync individual input names:

    * hold down the **TAB** key when plugging in your input property, objects, or collection.
      To automatically sync all input names:
    * right-click the **Create Properties** or **Create Collection** node.
    * select **Inherit all names**
      The **Inherit all names** option will lock input name editing, and always keep your input names synced with their sources.

  </Accordion>

  <Accordion title="How do I create new projects or models to publish to?">
    Currently, it's not possible to create new projects or models in Grasshopper. All project management should be done in your web browser.
  </Accordion>

  <Accordion title="Can I create specific objects for other applications like Revit or ETABs?">
    All models published in Grasshopper will only contain geometry, and will be loaded as geometry with render materials and colors in other applications (and properties, if Rhino or PowerBI).
    We do not currently support customizing objects for specific applications.
  </Accordion>

  <Accordion title="How do I change my account?">
    Right click your **Speckle Model URL** node and select **Change accounts** to change your account.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Tip>
  Full documentation of all Grasshopper nodes and sample scripts are installed with your connector.
  Navigate to **File** > **Special Folders** > **Components Folder** > **Speckle Sample Files** in Grasshopper to find them.
</Tip>

<Steps>
  <Step title="Get your Speckle model link">
    1. Add a **Speckle Model URL** node to the canvas.
    2. Choose a project:
       * Click on the **Project** button to select a project from the dropdown
       * or use the search bar to find another project.
    3. Choose a model:
       * Click on the **Model** button to select a model from the dropdown
       * or use the search bar to find another model.
    4. Choose a version:
       * Latest version is loaded by default.
       * To load a specific version, click on the **Version** button and select.
  </Step>

  <Step title="Load your model">
    1. Add a **Load** node to the canvas and connect your input:

    * Add your **Speckle Model URL** output to the Model Link input.

    2. Click **Load**.
       Your selected model version is now loaded in Grasshopper.

  </Step>

  <Step title="Get your model objects">
    1. Add a **Query objects** node to the canvas and connect your input:

    * Add your **Load** output to the collection input.

    2. You can now work with your loaded objects in Grasshopper.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/grasshopper_load.jpg" alt="Grasshopper load" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How do I access object fields that I see in the web browser, but that are not in my Grasshopper object properties?">
    If you want to access geometry properties like what you would see in **dev mode** in your browser, you can use the **Deconstruct** node.
    However, if you are looking for fields on a **DataObject** - e.g. the location curve of a **RevitObject**, they currently cannot be accessed in Grasshopper.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Copy your URL to a **Panel** and connect it to your **Speckle Model URL** node.
  </Accordion>

  <Accordion title="How do I change my account?">
    Right click your **Speckle Model URL** node and select **Change accounts** to change your account.
  </Accordion>
</AccordionGroup>

# Installing Connectors

Source: https://docs.speckle.systems/connectors/installation

Follow these steps to download and install a Speckle connector

<Steps>
  <Step title="Create a Speckle Account">
    Go to [speckle.systems](https://app.speckle.systems/) and create an account.
  </Step>

  <Step title="Download the connector">
    1. Go to [speckle.systems/connectors](https://app.speckle.systems/connectors).
    2. Download the connector for your software, such as Revit, Rhino, or Archicad. [See all supported software](https://www.speckle.systems/connectors).
  </Step>

  <Step title="Install the connector">
    <Warning>Please ensure that the target software is closed during the installation process.</Warning>
    <Warning>Do not use **Run as administrator** to install. This will not install the connector for your user.</Warning>

    1. Double-click the downloaded `.exe` or right-click and select **Open** to run the installer.
    2. Follow the on-screen prompts to complete installation.

  </Step>
</Steps>

<Info>Connectors are currently available for **Windows only**.</Info>

<Frame>
  <iframe width="100%" height="415" src="https://www.youtube.com/embed/mjYtKTo0fQU" title="Speckle Connector Installation" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen />
</Frame>

# How to use Speckle for Navisworks

Source: https://docs.speckle.systems/connectors/navisworks

Step-by-step guide for using the Navisworks connector

export const app_3 = "Navisworks"

export const app_2 = "Navisworks"

export const app_1 = "Navisworks"

export const app_0 = "Navisworks"

export const versions_0 = "2020, 2021, 2022, 2023, 2024, 2025 & 2026"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Navisworks connector">
    1. In Navisworks, select the **Speckle** tab in the ribbon.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/navisworks_toolbar.jpg" alt="Navisworks toolbar" />
    </Frame>

    2. Select **Speckle** to open the Navisworks connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of elements can I publish from Navisworks to Speckle?">
    All visible objects in the Navisworks scene can be published to Speckle. This
    includes geometry from appended NWC, DWG, IFC, and RVT files. The export
    includes: - object geometry (as meshes) - model hierarchy - attached
    properties (from source files) - file metadata
  </Accordion>

  <Accordion title="Can I publish only selected objects or specific appended files?">
    You can publish any of the following:

    <ul>
      <li>A manual selection of objects, which can include a file in the scene.</li>
      <li>A saved selection set</li>
      <li>A saved search set</li>
      <li>A saved view</li>
    </ul>

    Use the connector UI to choose which of these to send to Speckle.

  </Accordion>

  <Accordion title="Can I include saved timeliner information, redlines, or clash results?">
    Not at this time. The Navisworks connector currently focuses on object
    geometry and properties. Markups and clash results are not exported.
  </Accordion>

  <Accordion title="Can I preserve selection sets or search sets when publishing?">
    While selection and search sets themselves are not preserved as named sets in
    Speckle, as that concept doesn't yet exist on the web, you can use them as
    filters to choose what objects to send. The objects they reference will be
    exported with full geometry and metadata.
  </Accordion>

  <Accordion title="How do I ensure my Navisworks model is correctly positioned in Speckle?">
    The connector uses the world coordinate system as defined in Navisworks. If
    your model has an offset origin, it will be preserved in the Speckle model. To
    align with other models, ensure a consistent shared coordinate system.
  </Accordion>

  <Accordion title="My Navisworks model is in real-world coordinates, how can I move it closer to the origin?">
    You can use the **Transform** option in the Speckle connector to apply a
    translation to your model before publishing. This allows you to adjust the
    position without modifying the original Navisworks file.
  </Accordion>

  <Accordion title="Do custom properties (e.g., element metadata or quantities) get published?">
    Yes. All custom properties attached to elements in Navisworks are included in
    the Speckle export. These can be viewed in the Speckle web viewer by selecting
    an object and inspecting its properties.
  </Accordion>

  <Accordion title="Will properties added with DataTools be sent?">
    Yes, any properties added to objects using DataTools in Navisworks will be
    included in the export to Speckle. Ensure the properties are visible in the
    object inspector before publishing.
  </Accordion>

  <Accordion title="Can I export the model as a tree structure or a flat list?">
    By default, the connector exports objects as a flat list. If you want to
    preserve the model's hierarchy (tree structure), enable the **Preserve Hierarchy**
    option in the connector UI before publishing. Regardless of this setting, all
    elements will include a <code>path</code> property that records their original
    hierarchy within the model.
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Note>The {app_3} connector is publish-only.</Note>
If you would like to be able to load a model into {app_3}, please reach out on our Community Forum: [https://speckle.community/c/features](https://speckle.community/c/features/7)
Include the following information:

-   Which application your Speckle model is published from
-   Why you want to load your model into {app_3}
-   How frequently you would use this workflow (daily, weekly, monthly, longer).

# How to use Speckle for Power BI

Source: https://docs.speckle.systems/connectors/power-bi

Step-by-step guide for using the Power BI connector

export const app_1 = "Power BI"

export const app_0 = "Power BI"

export const versions_0 = "2020, 2021, 2022, 2023, 2024, 2025 & 2026"

export const os_0 = "Windows"

Speckle's connection to Power BI consists of two parts.

-   The **Power BI connector** lets you easily load your model from Speckle into Power BI in a tabular format.
-   The **3D Viewer Visual** allows you to view and color your models in 3d.

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Power BI connector">
    1. Select **Get Data**. 2. In the search box, enter *Speckle*. 3. Select
       **Connect to Speckle** and click **Connect**.
  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why don't I see Speckle as a data source in Power BI?">
    You need to enable third-party data sources. 1. Go to **File** > **Options
    and settings** > **Options** > **Security**. 2. Under **Data Extensions**,
    select **Allow any extension to load without validation or warning**.

    <div style={{ position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden' }}>
      <iframe
        src="https://player.vimeo.com/video/1090885358"
        allowFullScreen
        loading="lazy"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          }}
      />
    </div>

  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Load from Speckle">
    1. Copy Model URL from the web app.
    2. Paste it in the text field and select **OK**.
  </Step>

  <Step title="Import 3D Visual">
    1. In the Visualizations pane, select the three dots **(...),** then select **Import a visual from a file**.
    2. Browse to `Documents/Power BI Desktop/Custom Visuals`.
    3. Select `Speckle 3D Visual.pbiviz` and **Open**.
  </Step>

  <Step title="Visualize a model">
    1. In the **Visualizations** pane, select **Speckle 3D Visual**
    2. Configure the visual:
       * Drag *Version Object ID* column into the **Version Object ID** input -> required for **viewing**
       * Drag *Object IDs* column into the **Object IDs** input ->  required for **interactivity**
       * Drag any column into **Tooltip** input -> for **tooltip**
       * Drag any column into **Color by** input -> for **coloring** model
    3. Wait for your model to load in the viewer
  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Where do I find the 3D visual?">
    You'll find Speckle's 3D visual in the **Documents/Power BI Desktop/Custom Visuals** folder.
  </Accordion>

  <Accordion title="Where's the Model URL in the new Power BI connector?">
    The next-generation Power BI connector doesn't use Model URL input. You can safely ignore it.
  </Accordion>

  <Accordion title="Why do I get an 'Access to the resource is forbidden' error?">
    This is a browser-related issue. To fix it:

    1. Go to **File** > **Options and settings** > **Options** > **Security**
    2. Under **Authentication Browser**, clear **Use my default web browser**

  </Accordion>

  <Accordion title="Why do I get a 'Permission denied' error?">
    You don't have the required permissions to load the model. Contact the project owner and ask them to give you the necessary permissions.
  </Accordion>

  <Accordion title="Why do I get an 'Unable to connect remote server' error?">
    The Power BI connector needs Speckle Desktop Service to run on your machine. Make sure Desktop Service is active and running.
  </Accordion>

  <Accordion title="Can I load and visualize private projects with the Power BI connector?">
    Yes. Both the Power BI connector and 3D visual support private projects.
  </Accordion>

  <Accordion title="Why doesn't my report update after a new version is published?">
    Following reasons might cause this issue:

    1. Refresh preview
       Make sure you clicked **Refresh** in the Power BI ribbon to load the latest version.

    2. Check if you loaded a specific version
       If your model URL contains an "@" symbol, this means you loaded a specific version. Power BI connector will only load that specific version and not any new versions.

  </Accordion>

  <Accordion title="How do I visualize multiple models in Power BI?">
    Here's how you can load and visualize multiple models with Power BI connector:

    1. First, federate your models in the web app.
    2. Copy the federated model URL
    3. Load federated model in Power BI.

    Visualizing multiple models in Power BI is similar to visualizing a single model.

  </Accordion>

  <Accordion title="How do I control the visibility of unselected elements in the 3D visual?">
    Use the ghost icon in the 3D visual. By default, unselected elements appear ghosted. Clear the ghost icon to completely hide unselected elements.
  </Accordion>

  <Accordion title="How do I hide the Speckle logo from the 3D visual?">
    If you have a Business plan, you can hide Speckle branding by selecting the arrow in the top bar. Free plan users can't hide the Speckle logo.
  </Accordion>

  <Accordion title="Why can I view a model in Speckle but can't load it in Power BI?">
    Viewing and loading a model require different permissions. To load a model in a connector, contact the project owner to change your project role.
  </Accordion>
</AccordionGroup>

# How to use Speckle for Revit

Source: https://docs.speckle.systems/connectors/revit

Step-by-step guide for using the Revit connector

export const app_4 = "Revit"

export const app_3 = "Revit"

export const app_2 = "Revit"

export const app_1 = "Revit"

export const app_0 = "Revit"

export const versions_0 = "2022, 2023, 2024, 2025 & 🆕2026"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Revit connector">
    1. In Revit, select the **Speckle** tab in the ribbon.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/revit_toolbar.jpg" alt="Revit toolbar" />
    </Frame>

    2. Select **Speckle** to open the Revit connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of Revit elements can I publish to Speckle?">
    All visible elements in the Model category (such as walls, floors, beams, and columns) can be published. In the Annotation category, only visible gridlines can be published. Each element contains the following information:

    * category, family, and type
    * level
    * location curve (if any)
    * Mesh (solid elements), Curve (model curves), or Pointcloud geometry
    * custom properties
    * render material

  </Accordion>

  <Accordion title="How do I publish models from Revit views?">
    1. Click the blue **filter** field at the top of **Select objects** dialog while publishing a new version.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/revit_filters.jpg" alt="Revit filters" />
    </Frame>

    2. Select **Views**, and then select the view you would like to publish from.

  </Accordion>

  <Accordion title="How do I publish models by Revit category?">
    1. Click the blue **filter** field at the top of **Select objects** dialog while publishing a new version.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/revit_filters.jpg" alt="Revit filters" />
    </Frame>

    2. Select **Categories**, and then click on any number of categories you would like to add to the filter.

  </Accordion>

  <Accordion title="How do I publish linked models?">
    Linked models are supported by default when publishing. If they are not included in your published version:

    1. Expand the **Settings** field at the bottom of the **Select objects** dialog while publishing a new version.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/revit_settings.jpg" alt="Revit settings" />
    </Frame>

    2. Check that the **Include linked models** toggle is turned on.

  </Accordion>

  <Accordion title="How do I make sure my Revit model is aligned with my other Speckle models?">
    If you are using reference points to coordinate your project, you can publish your Revit model according to a specific reference point:

    1. Expand the **Settings** field at the bottom of the **Select objects** dialog while publishing a new version.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/revit_settings.jpg" alt="Revit settings" />
    </Frame>

    2. Set the **Reference Point** setting to your desired reference point.
       Your published model will now be oriented according to your specified reference point.

  </Accordion>

  <Accordion title="How do I see the custom properties on my published Revit elements, like parameters or material quantities?">
    All custom properties can be found under the `properties` field when you select and view a Revit object in your browser.
    Custom properties vary depending on the type of Revit element, and can include:

    * element id, built-in category, and workset properties
    * material quantities
    * parameters
    * structural material properties (such as density and compressive strength)

  </Accordion>

  <Accordion title="How do I publish my rebar as solid objects instead of curves?">
    1. Expand the **Settings** field at the bottom of the **Select objects** dialog while publishing a new version.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/revit_settings.jpg" alt="Revit settings" />
    </Frame>

    2. Toggle the **Send Rebars As Volumetric** setting to true.
       Caution: publishing all rebars as their volumetric representations can significantly slow down publishing speed.

  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Select Load">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_1.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_2.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a model">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_3.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a version to load">
    * Latest version is always first.
    * To load a specific version, select it from the UI.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_4.jpg" alt="Load" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_5.jpg" alt="Load" />
    </Frame>

    Your selected model is now loaded in {app_3}.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How are Speckle models loaded in Revit?">
    All objects in Speckle models are loaded as Direct Shapes (generic models) with a default category in Revit. If your model contains block instances, each instance will be loaded as its own generic model. Each object will be loaded with:

    * render material (if any)
    * `Mesh`, `Curve`, or `Solid` (only from Rhino and Grasshopper) geometry.

  </Accordion>

  <Accordion title="Can I load custom properties in Revit, like parameters?">
    Currently, you can not load any custom properties on your Speckle model objects into Revit.
  </Accordion>

  <Accordion title="How do I load a Speckle Model according to a specific reference point in Revit?">
    If you are loading a Speckle Revit model that was published with a reference point, the model will be loaded according to the transformation of that reference point.
    Any existing reference points in your Revit document will be ignored.
    Models published from other applications cannot be loaded according to a reference point in your Revit document.
  </Accordion>

  <Accordion title="How do I change the material of a Speckle model object I loaded in Revit?">
    If your Speckle model was published from Rhino or Grasshopper, it will contain
    solid geometry and you can edit the material of the created direct shape as
    you'd like. For any other Speckle model, currently it is not possible to
    change the applied material.
  </Accordion>

  <Accordion title="How do I change the category of a Speckle model object I loaded in Revit?">
    Currently, you can not change the category of a loaded object.
  </Accordion>

  <Accordion title="Why are some objects that I loaded missing from my model?">
    After you load a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for loading in {app_4}.
  </Accordion>

  <Accordion title="Why can't I select a project in the UI—it's disabled?">
    This happens when you don't have permissions to load a project. Contact the project owner to change your role.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Next to the search box in the project selection dialog, there's an **Add model by URL** option. Paste the model URL there.
  </Accordion>
</AccordionGroup>

# How to use Speckle for Rhino

Source: https://docs.speckle.systems/connectors/rhino

Step-by-step guide for using the Rhino connector

export const app_4 = "Rhino"

export const app_3 = "Rhino"

export const app_2 = "Rhino"

export const app_1 = "Rhino"

export const app_0 = "Rhino"

export const versions_0 = "7 & 8"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Tip>
  {' '}

The **Rhino** and **Grasshopper** connectors are bundled, so if you installed one,
you don't need to install the other.
</Tip>

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Rhino connector">
    1. Type **Speckle** in the command line, or 2. Select **Speckle** in the
       Speckle Toolbar to open the Rhino connector.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/rhino_toolbar.jpg" alt="Rhino toolbar" />
    </Frame>

    3. Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Where is the Speckle toolbar in Rhino?">
    After installation, if you don't see the Speckle Rhino toolbar, you can manually load it:

    1. Type the **Toolbar** command in Rhino.
    2. Select **File** > **Open** and navigate to your Rhino UI folder: `AppData\Roaming\McNeel\Rhinoceros\7.0\UI\Plug-ins`
    3. Select the **Speckle.Connectors.Rhino.rui** file and press **Enter**.

    You should now see the toolbar in Rhino.

  </Accordion>

  <Accordion title="I'm getting a framework compatibility error or a black connector window">
    Early versions of Rhino 8 may not have propery framework compatibility for plugins.
    We advise you to upgrade to Rhino 8.9 and above if you are using an earlier version.
    You can also change your Rhino runtime:

    1. Type the **SetDotNetRuntime** command in Rhino
    2. Select the **NETFramework** option
    3. Restart Rhino

  </Accordion>

  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of Rhino elements can I publish to Speckle??">
    All types of visible geometry can be published, as well as `hatch`, `text`, and `blocks`. Each published object contains the following information:

    * Name
    * Color
    * Render material
    * User strings

  </Accordion>

  <Accordion title="How do I publish models from Rhino layers?">
    1. Click the blue **filter** field at the top of **Select objects** dialog while publishing a new version.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/rhino_filters.jpg" alt="Rhino filters" />
    </Frame>

    2. Select **Layers**, and then click on any number of layers you would like to add to the filter.

  </Accordion>

  <Accordion title="How do I see the user strings on my published Rhino objects?">
    All custom properties can be found under the **properties** field when you select and view a Rhino object in your browser.
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Select Load">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_1.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_2.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a model">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_3.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a version to load">
    * Latest version is always first.
    * To load a specific version, select it from the UI.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_4.jpg" alt="Load" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_5.jpg" alt="Load" />
    </Frame>

    Your selected model is now loaded in {app_3}.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How are Speckle models loaded in Rhino?">
    All objects in Speckle models are loaded as `geometry`, `text`, or `blocks` in Rhino. They're created in the same layer structure as what you see when viewing your model in your browser. Each object will be loaded with:

    * Render material (if any)
    * Color (if any)
    * Name (if set)
    * Custom properties as user strings

  </Accordion>

  <Accordion title="Can I load custom properties in Rhino, like Revit parameters?">
    Yes, all custom properties found under the **properties** field will be created as user strings in Rhino.
  </Accordion>

  <Accordion title="Why are some objects that I loaded missing from my model?">
    After you load a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for loading in {app_4}.
  </Accordion>

  <Accordion title="Why can't I select a project in the UI—it's disabled?">
    This happens when you don't have permissions to load a project. Contact the project owner to change your role.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Next to the search box in the project selection dialog, there's an **Add model by URL** option. Paste the model URL there.
  </Accordion>
</AccordionGroup>

# How to use Speckle for SketchUp

Source: https://docs.speckle.systems/connectors/sketchup

Step-by-step guide for using the SketchUp connector

export const app_4 = "SketchUp"

export const app_3 = "SketchUp"

export const app_2 = "SketchUp"

export const app_1 = "SketchUp"

export const app_0 = "SketchUp"

export const versions_0 = "2021, 2022, 2023, 2024, & 2025"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the SketchUp connector">
    1. Navigate to **Extensions** > **Speckle**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/sketchup_toolbar.jpg" alt="SketchUp toolbar" />
    </Frame>

    2. Select **Initialize Speckle** to open the SketchUp connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of SketchUp elements can I publish to Speckle?">
    You can publish all types of `components`, `groups`, `faces`, and `lines` to Speckle. Each published object includes:

    * Custom user attributes
    * Render materials

  </Accordion>

  <Accordion title="How do I see custom user attributes on my published SketchUp objects?">
    Select an object in your browser and look under the **properties** field to view all user attributes.
  </Accordion>

  <Accordion title="Why aren't my SketchUp materials applied correctly when loaded in other applications?">
    This usually happens when you apply materials to **components** instead of their faces. Apply materials to **faces** for correct display in other applications.
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Steps>
  <Step title="Select Load">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_1.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_2.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a model">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_3.jpg" alt="Load" />
    </Frame>
  </Step>

  <Step title="Choose a version to load">
    * Latest version is always first.
    * To load a specific version, select it from the UI.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_4.jpg" alt="Load" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_load_5.jpg" alt="Load" />
    </Frame>

    Your selected model is now loaded in {app_3}.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="How are Speckle models loaded in SketchUp?">
    All objects in Speckle models are loaded as Components in SketchUp. They're created with the same layers you see when viewing your model in the browser.

    * Name of the object is loaded as component name
    * Render materials are applied.
    * Properties are loaded as user attributes.

  </Accordion>

  <Accordion title="Are properties from other applications, like Revit parameters, loaded in SketchUp?">
    Yes, all parameters found under the **properties** field are loaded as user attributes in SketchUp.
  </Accordion>

  <Accordion title="How do I see the user attributes on my loaded SketchUp objects?">
    To view them, you can use [Attribute Helper](https://extensions.sketchup.com/extension/f4d9d053-4479-4a9a-90da-b79fa16e28c4/attribute-helper) plugin from SketchUp.
  </Accordion>

  <Accordion title="Why are some objects that I loaded missing from my model?">
    After you load a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for loading in {app_4}.
  </Accordion>

  <Accordion title="Why can't I select a project in the UI—it's disabled?">
    This happens when you don't have permissions to load a project. Contact the project owner to change your role.
  </Accordion>

  <Accordion title="Can I load a model via URL?">
    Yes. Next to the search box in the project selection dialog, there's an **Add model by URL** option. Paste the model URL there.
  </Accordion>
</AccordionGroup>

# How to use Speckle for Tekla Structures

Source: https://docs.speckle.systems/connectors/tekla

Step-by-step guide for using the Tekla Structures connector

export const app_3 = "Tekla Structures"

export const app_2 = "Tekla Structures"

export const app_1 = "Tekla Structures"

export const app_0 = "Tekla Structures"

export const versions_0 = "2023, 2024 & 2025"

export const os_0 = "Windows"

<Info>
  Speckle currently supports {app_0} versions: **{versions_0}**.
  The {app_0} connector works on **{os_0}** only.
</Info>

## Setup

<Steps>
  <Step title="Install the connector">
    Install your [{app_1} connector](/connectors/installation)
  </Step>

  <Step title="Open the Tekla Structures connector">
    1. In Tekla Structures, select the **Speckle** tab in the ribbon.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/tekla_toolbar.jpg" alt="Tekla toolbar" />
    </Frame>

    2. Select **Speckle** to open the Tekla Structures connector.

    3) Select **Sign in** if you haven't linked your Speckle account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_login.jpg" alt="Login" />
    </Frame>

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    1. Make sure your version of {app_2} is one of the supported versions.
    2. Uninstall and [reinstall your connector](/connectors/installation).

    Note: Make sure you are **not** selecting **Run as administrator** when installing - this will install for the administrator user, and not your own user.
    Instead, double-click the `.exe` or right-clicking and then selecting `Open` to run the installer.
    Installation issues can also be caused by conflicting plugins.

    If you're still experiencing problems, please report it in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    If your connector window is floating, **try docking it to your application** to fix blank UI issues.

    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`.
    Please report your problem in our [Community Forum](https://speckle.community/c/help) and include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="Why can't I add a new account?">
    This can happen if our **desktop service** isn't running. Desktop Service is used for authenticating new accounts. If it's not running, search for **Speckle Desktop Services** in Windows search and run it.
  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove **Speckle Desktop Services** as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector [in the web app](https://app.speckle.systems/connectors).
    If a new version of the connector is available, you will also see a notification in your connector UI.
  </Accordion>
</AccordionGroup>

## Publishing a Model

<Steps>
  <Step title="Select Publish">
    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_1.jpg" alt="Publish" />
    </Frame>
  </Step>

  <Step title="Choose a project">
    * Select an existing project
    * or select **New Project** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_2.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Choose a model">
    * Select an existing model
    * or select **New Model** to create one

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_3.jpg" alt="Publish" />
    </Frame>

  </Step>

  <Step title="Select objects to publish">
    1. In your application viewport, select the elements you want to publish.
    2. Select **Publish**.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_4.jpg" alt="Publish" />
    </Frame>

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/connectors/dui_publish_5.jpg" alt="Publish" />
    </Frame>

    3. Your model is now published to Speckle and is available to the rest of your team.

  </Step>
</Steps>

<AccordionGroup>
  <Accordion title="What types of Tekla Structures objects can I publish to Speckle?">
    All selectable model objects can be published, such as beams, plates, and bolts. Each object is published as a `TeklaObject` and contains the following information:

    * Type
    * Render Material
    * Custom Properties (e.g. Report)

  </Accordion>

  <Accordion title="How do I see the custom properties on my published Tekla Structures objects, like reports?">
    All custom properties can be found under the `properties` field when you select and view a Tekla Structures object in your browser.Custom properties vary depending on the type of object, and can include:

    * Report (e.g. `Area`, `Volume`, or `Phase`)
    * User-Defined Attributes
    * Beams: `profile` and `material`

  </Accordion>

  <Accordion title="Which object properties do not get published with the Tekla Structures connector?">
    Currently\*\*,\*\* the following properties are *not* published on objects:

    * Assemblies
    * Drawing layout and title blocks
    * Numbering series and sequence settings

  </Accordion>

  <Accordion title="Can I publish objects from a drawing view?">
    No, you can not publish from drawing views.
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the **View Modes** button in the side bar, and switch the view mode to **Shaded**. If you still don't see your object colors, let us know in our [Community Forum](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published missing from my model?">
    After you publish a Speckle model, click on the **Report** button to see any errors that may have occurred.
    Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing.
  </Accordion>
</AccordionGroup>

## Loading a Model

<Note>The {app_3} connector is publish-only.</Note>
If you would like to be able to load a model into {app_3}, please reach out on our Community Forum: [https://speckle.community/c/features](https://speckle.community/c/features/7)
Include the following information:

-   Which application your Speckle model is published from
-   Why you want to load your model into {app_3}
-   How frequently you would use this workflow (daily, weekly, monthly, longer).

# Looking for developer docs?

Source: https://docs.speckle.systems/dev/looking-for-developer-docs

We're working on it!

export const tag_2 = "Legacy"

export const tag_1 = "Current"

export const tag_0 = "Current"

Our powerful SDKs have been updated to support the next gen connectors and
data models. We will be bringing back some of your favourite examples and guides.

Example use-cases for developing with Speckle:

-   Building your own applications or integrations.
-   Automating tasks.
-   Custom web apps and visualisations.
-   Data pipelining and ETL.
-   Robotics and 3D printing.
-   Data analysis and machine learning.

In the meantime, you can find our older docs including the viewer API, server deployment and legacy SDKs in the [Developer Hub](https://speckle.guide/dev/).

<h4>
  <a href="https://speckle.guide/viewer">Our Viewer API docs</a>{' '}

  <span class="px-1.5 py-0.5 mr-2 align-top rounded-md text-[0.7rem] text-primary-dark dark:text-primary-light leading-tight font-semibold bg-primary/10 flex-shrink-0">
    {tag_0}
  </span>
</h4>

These are current and valid today and waiting for migration. Use them to build your own applications or implement Speckle in your own platform.

<h4>
  <a href="https://speckle.guide/server">Our server deployment docs</a>{' '}

  <span class="px-1.5 py-0.5 mr-2 align-top rounded-md text-[0.7rem] text-primary-dark dark:text-primary-light leading-tight font-semibold bg-primary/10 flex-shrink-0">
    {tag_1}
  </span>
</h4>

Learn how to deploy your own Speckle server using the open-source Speckle Server
via Docker or Kubernetes.

<h4>
  <a href="https://speckle.guide/">Our legacy SDKs docs</a> <Tag tag="Legacy" />
</h4>

Our older SDKs for Speckle.

<h4>
  <a href="https://speckle.guide/automate">Our Speckle Automate docs</a>{' '}

  <span class="px-1.5 py-0.5 mr-2 align-top rounded-md text-[0.7rem] text-primary-dark dark:text-primary-light leading-tight font-semibold bg-primary/10 flex-shrink-0">
    {tag_2}
  </span>
</h4>

Our newer serverless automation tool.

# Frequently Asked Questions

Source: https://docs.speckle.systems/quickstart/faq

We've collected commonly asked questions that you might have as you get started.

export const app_0 = undefined

## Projects, Models and Versions

### Projects

<AccordionGroup>
  <Accordion title="Is there a limit to the number of projects I can create?">
    The number of projects you can create is subject only to the limits of your workspace.
  </Accordion>

  <Accordion title="Can I delete a project?">
    Yes, you can delete a project by selecting the project from the projects list
    page and clicking the **Delete project** button.

    <Warning>
      Deleting a project is destructive. It will delete all the data associated with it.
    </Warning>

  </Accordion>

  <Accordion title="Can I rename a project?">
    Yes, if you the project owner, you can rename a project by selecting the
    project from the projects list page and clicking the **Rename project**
    button.
  </Accordion>

  <Accordion title="Can I move a project to another workspace?">
    No, not in the web interface, if this is something you need critically,
    contact us either in the application chat or by email at [support@speckle.com](mailto:support@speckle.com) A
    project made in the personal projects era can be migrated one time to a
    workspace.
  </Accordion>

  <Accordion title="If I rename a project will it break anything?">
    No, it will not break anything. The only thing that will be affected is the
    name of the project.
  </Accordion>

  <Accordion title="Can I enforce naming conventions to project names?">
    No, you cannot enforce naming conventions to project names.
  </Accordion>

  <Accordion title="Can I change the description of a project?">
    Yes, you can change the description of a project by selecting the project from
    the projects list page and clicking the **Edit project** button.
  </Accordion>

  <Accordion title="Is there a limit to the number of members in a project?">
    No, there is no limit to the number of members in a project. However, depending on your
    **workspace plan** you may be charged for additional project members not already in your workspace.

    You can add as many **viewers** to your project as you like, they are free.

  </Accordion>
</AccordionGroup>

### Models

<AccordionGroup>
  <Accordion title="Can I choose who can edit specific models?">
    No, edit rights are set at the project level only at this time.
  </Accordion>

  <Accordion title="Can I set a model as read-only?">
    No, read-only status is set at the project level only at this time.
  </Accordion>

  <Accordion title="Why use multiple models?">
    Here are a few common reasons:

    * **Split by discipline**: For large projects, separate models by team, e.g., <em>Architecture</em>, <em>Structural</em>, and <em>MEP</em>. This ensures each team receives only what’s relevant.
    * **Split by building**: If your project includes multiple buildings, keep them in one project but create separate models like <em>Building A</em>, <em>Building B</em>, and <em>Building C</em>.
    * **Explore design options**: Want to present different façade concepts? Create models like <em>Option A</em>, <em>Option B</em>, and <em>Option C</em> and switch between them to show your client.

  </Accordion>

  <Accordion title="What does 'federating models' mean?">
    In Speckle, you can <strong>federate models</strong> by loading multiple models into the same view — even if created separately.
    This is useful for working with different teams or disciplines. For example, view the <em>architecture</em>, <em>structure</em>, and <em>MEP</em> models together in a single, coordinated view without merging them into one file.

    Federating models helps you:

    * Compare design options
    * Coordinate between disciplines
    * Keep models separate while viewing them side by side
      You can do this directly in the <strong>Speckle 3D viewer</strong> or in supported
      design tools using our **connectors**.

  </Accordion>

  <Accordion title="How do I create and manage models?">
    You can create as many models as needed within a project. The Speckle Web App makes it simple to:

    * Add new models
    * Rename models
    * Switch between models
      This helps you keep your work organised and ensures each model is used as intended.

  </Accordion>

  <Accordion title="How do I delete a model?">
    You can delete a model by selecting the **Delete model** button in the model settings drop-down found on the models list page.
    This will remove the model from the project and **all associated data**.
  </Accordion>

  <Accordion title="How many models can I have in a project?">
    You can have as many models as you need in a project. However, the number of models you have in total in your workspace
    across all projects may be limited by your workspace plan.
  </Accordion>

  <Accordion title="How do I switch between models?">
    You can switch between models by selecting the model from the models list page.
    This will open the model in the Speckle Web Viewer.
  </Accordion>

  <Accordion title="Can I rename a model?">
    Yes, you can rename a model by selecting the model from the models list page and clicking the **Rename model** button.
  </Accordion>

  <Accordion title="How do I move a model to another folder?">
    You can move a model to another folder by selecting the model from the models list
    page and clicking the **Rename model** button.
    It is the presence of `/`s in the model name that determines the folder structure.
  </Accordion>

  <Accordion title="How many folders can I have?">
    You can have as many folders as you need in a project. It is the presence of `/`s in the
    model name that determines the folder structure. However, it may be preferable to only use
    one or two levels of folders to keep your models organised.
  </Accordion>

  <Accordion title="Is there a maximum size for a model?">
    Theoretically no, but the performance of the 3D viewer will be impacted if it is large number of
    extremelly detailed objects. It can be benefical to break models up and federate them together
    as required to keep the performance high.
  </Accordion>
</AccordionGroup>

### Versions

<AccordionGroup>
  <Accordion title="Can I set an approval status on a version?">
    You can only set the version message, potentially to something meaningful like "Approved for release".
  </Accordion>

  <Accordion title="How long are versions stored for?">
    Versions are stored indefinitely, but you may be limited as to how many you can see depending on your workspace plan.
  </Accordion>

  <Accordion title="Can I prevent others from seeing specific versions?">
    No, once a version is published it is visible to all users with permission to view the model.
  </Accordion>

  <Accordion title="Can I prevent others from deleting versions?">
    Only the owner of the model can delete versions.
  </Accordion>

  <Accordion title="How many versions can I publish?">
    You can publish as many versions as you want, but you may be limited as to how many you can see.
  </Accordion>

  <Accordion title="I already published a version, can I still set or edit its version message?">
    Yes, you can set or edit the version message for any version from the version history page.
  </Accordion>

  <Accordion title="I can't see older versions">
    All older versions are stored indefinitely but may be hidden if depending on your workspace plan limits.
  </Accordion>

  <Accordion title="How do I visually compare versions?">
    You can compare two versions to see the differences between them. This is useful to review changes,
    or to see what changed between two specific points in time. You can do this in the 3D viewer, more details
    can be found in the [compare versions](/3d-viewer/compare-versions) page.
  </Accordion>

  <Accordion title="How do I delete a version?">
    If you've published a version by mistake you can delete it. This will remove it from the model
    and if you delete the latest version it will make the previous version the latest.
  </Accordion>

  <Accordion title="How do I restore a version?">
    You can't promote a specific version to be the latest, but you can publish a new version
    which will become the latest. Or delete all newer versions. Receiving a specific
    version and re-publishing it will theoretically restore it, but this can be a lossy
    process depending on the connector. More reliable would be to do so programmatically.
  </Accordion>

  <Accordion title="How do I set a version message?">
    You will prompted in your connector to set a version message when you publish.
  </Accordion>
</AccordionGroup>

## Permissions and Roles

### Workspace roles

<AccordionGroup>
  <Accordion title="What is a workspace role?">
    A workspace role is a role that determines what actions a user can perform within a workspace.
  </Accordion>

  <Accordion title="What are guest roles?">
    Guest roles are a type of workspace role that allows users to view and comment on models in a workspace.
  </Accordion>

  <Accordion title="How do I invite someone to my workspace?">
    You can invite someone to your workspace by clicking the **Invite** button in the top right corner of the workspace page.

    You can also set your workspace to allow self-signup by making your workspace **domain discoverable**.
    Users with an email domain matching what you have verified to the workspace will be notified your
    workspace exists and can request to join. You can also set it up to automatically add them to the workspace without admin approval.

    <Note>
      Only admins can invite users to a workspace.
    </Note>

    Learn more about [inviting users to a workspace](/workspaces/inviting).

  </Accordion>

  <Accordion title="How do I remove someone from my workspace?">
    You can remove someone from your workspace by clicking the **Remove** button in the top right corner of the workspace page.
  </Accordion>
</AccordionGroup>

### Project roles

<AccordionGroup>
  <Accordion title="Can non-workspace members have a project role?">
    You can add anyone to a project role if it is allowable by the workspace security settings.
    If a user is added to a project as member who **can edit** they will be added as an editor
    to the workspace. If they are not a member of the workspace they will be added as a guest.
  </Accordion>

  <Accordion title="Can I assign roles to teams?">
    No, roles are set on a member by member basis.
  </Accordion>
</AccordionGroup>

## Billing and Usage

### Seats

<AccordionGroup>
  <Accordion title="Can I swap seats between people?">
    Yes, within a billing cycle if a seat is removed from a workspace member or guest
    then it can be allocated to another.
    <Warning>Allocating a seat to a new member or guest without first unallocating will
    add a prorated cost for an additional seat for that billing cycle.</Warning>
  </Accordion>

  <Accordion title="What happens if I remove an editor seat from a user who is a project collaborator?">
    They will remain a project team member but their role will be downgraded to **can view**.
  </Accordion>

  <Accordion title="What happens if I remove an editor seat from a user who is a workspace member?">
    They will remain a workspace member but their role will be downgraded to **can view**. Their role
    on any projects they are a member of will also be downgraded to **can view**.
  </Accordion>
</AccordionGroup>

## Troubleshooting

### Connectors

Specific connector frequently asked questions can be found in each connector's usage guide.

<Columns cols={4}>
  <Card title="Revit" href="/connectors/revit/">
    Usage guide for publishing and loading Revit models.
  </Card>

  <Card title="Rhino" href="/connectors/rhino/">
    Usage guide for publishing and loading Rhino models.
  </Card>

  <Card title="Grasshopper" href="/connectors/grasshopper/">
    Usage guide for publishing and loading Grasshopper models.
  </Card>

  <Card title="Power BI" href="/connectors/power-bi/">
    Usage guide for loading models into Power BI.
  </Card>

  <Card title="Blender" href="/connectors/blender/">
    Usage guide for loading models into Blender.
  </Card>

  <Card title="Civil 3D" href="/connectors/civil3d/">
    Usage guide for publishing and loading Civil 3D models.
  </Card>

  <Card title="AutoCAD" href="/connectors/autocad/">
    Usage guide for publishing and loading AutoCAD models.
  </Card>

  <Card title="Archicad" href="/connectors/archicad/">
    Usage guide for publishing and loading Archicad models.
  </Card>

  <Card title="Tekla" href="/connectors/tekla/">
    Usage guide for publishing Tekla models.
  </Card>

  <Card title="ETABS" href="/connectors/etabs/">
    Usage guide for publishing ETABS models.
  </Card>

  <Card title="Navisworks" href="/connectors/navisworks/">
    Usage guide for publishing Navisworks models.
  </Card>

  <Card title="SketchUp" href="/connectors/sketchup/">
    Usage guide for publishing and loading SketchUp models.
  </Card>
</Columns>

#### General Connector Troubleshooting

<AccordionGroup>
  <Accordion title="Why is the Speckle plugin not showing up after I installed the connector?">
    Make sure your version of {app_0} is one of the supported versions. Installation issues are also sometimes caused by conflicting plugins. Please report your problem in our Community Forum: [https://speckle.community/c/help](https://speckle.community/c/help)

    And include the following information:

    * Your application version
    * Your Speckle connector version

  </Accordion>

  <Accordion title="Why did I get an error when using the Speckle command to open the connector?">
    If you still have the legacy version installed, make sure you have `version 2.23` or above. Any version below 2.23 will have conflicting commands with the AutoCAD connector.
  </Accordion>

  <Accordion title="Why does my model have the wrong colors in the web browser viewer?">
    In the viewer, select the `View Modes` button in the side bar, and switch the view mode to `Shaded`. If you still don't see your object colors, let us know in our Community Forum: [https://speckle.community/c/help](https://speckle.community/c/help)
  </Accordion>

  <Accordion title="Why are some objects that I published or loaded missing from my model?">
    After you publish or load a Speckle model, click on the `Report` button to see any errors that may have occurred. Click on any item in the report to highlight that item in your application. Some objects may not be supported for publishing or loading.
  </Accordion>

  <Accordion title="What should I do if the plugin UI is empty or unresponsive, or if my application crashes?">
    For major issues, you can sometimes find a `log` file in your directory at `AppData\Roaming\Speckle\Logs`. Please report your problem in our Community Forum: [https://speckle.community/c/help](https://speckle.community/c/help) And include the following information:

    * Your application version
    * Your Speckle connector version
    * A copy of the log

  </Accordion>

  <Accordion title="How do I uninstall my connector?">
    All Speckle connectors are installed like any other program. You can uninstall them directly from your system's `Applications`. For a full uninstall, you should also remove `Speckle Desktop Services` as well as your Speckle connector.
  </Accordion>

  <Accordion title="How do I update my connector to the latest version?">
    You can always download the latest version of the connector at [https://app.speckle.systems/connectors](https://app.speckle.systems/connectors). If a new version of the connector is available, you will also see a notification in your connector UI. \[@bilal need autoupdating behavior]
  </Accordion>

  <Accordion title="Where do I download Speckle Manager?">
    Speckle Manager has been deprecated and is no longer required to install connectors. It can still be [downloaded and used with legacy connectors](https://releases.speckle.systems/legacy-connectors).
  </Accordion>

  <Accordion title="How do I install connectors for Mac?">
    Connectors are currently available for Windows only.
  </Accordion>

  <Accordion title="I need more help!">
    You can always reach us by posting on our Community Forum: [https://speckle.community](https://speckle.community/). We try our best to respond as quickly as possible!
  </Accordion>
</AccordionGroup>

## How to Get Help

If you have any questions or issues not listed here, please contact us:

-   In-app support
-   Community support
    -   Report a bug
    -   Request a feature
    -   Ask a question
-   Business plan support
    -   Some plans include priority support.

# Quickstart Guide

Source: https://docs.speckle.systems/quickstart/quickstart

Get up and running with Speckle in no time!

<div style={{ position: 'relative', paddingBottom: '56.25%', height: 0, overflow: 'hidden' }}>
  <iframe
    src="https://player.vimeo.com/video/1084612464"
    allowFullScreen
    loading="lazy"
    style={{
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
  }}
  />
</div>

<Steps>
  <Step title="Create an account">
    Visit [speckle.systems](https://app.speckle.systems/) and sign up. You can join an existing workspace; otherwise, one will be created for you.
  </Step>

  <Step title="Install Connectors">
    Download and install [connectors](https://app.speckle.systems/connectors) for your software, for example, Power BI. You will need a connector to publish your first model (unless you prefer to upload an IFC, OBJ, or STL directly).

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/introduction/intro-short_power_bi.gif" alt="install" />
    </Frame>

    <Warning>Make sure that the target software is closed during the installation process.</Warning>

  </Step>

  <Step title="Launch the connector and log in">
    Launch the software and look for the **Speckle** tab or menu, then click the Speckle icon to open the Connector panel.

    You can now log in with your account.

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/introduction/intro-signing_up_for_revit_first_time.gif" alt="install" />
    </Frame>

    <Note>If you cannot find the Speckle connector, check the dedicated guide page for[the connector of your software](../connectors/overview).</Note>

  </Step>

  <Step title="Publish your first model">
    With the Speckle panel open, click **Publish**.

    Select the destination for your model:

    * **Workspace:** Pick a workspace
    * **Project:** Choose an existing project or click the **+** button to create a new one
    * **Model:** Select or create a model to use

    Finally, click **Publish** and view your model online!

    <Frame>
      <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/introduction/intro-publishing_into_speckle.gif" alt="install" />
    </Frame>

  </Step>
</Steps>

You're now ready to explore more advanced topics.

# Welcome to Speckle

Source: https://docs.speckle.systems/quickstart/welcome

This documentation is your go-to resource for basic understanding of Speckle's platform and terminology, getting started guides to set up workspaces, projects, and connectors, and common answers to FAQs and troubleshooting tips.

## What is Speckle?

Speckle is a unique design collaboration platform that replaces file-based workflows
with live connections between CAD and BIM tools. It keeps teams in sync without any
manual exports, version conflicts, or even the need for a specialized software license.

Speckle gives you a smarter and faster way to track, and automate design and building
data across tools, workflows, and stakeholders. Whether you're designing, engineering,
building, managing, or approving—Speckle makes your model data work for you, not against you.

## Why Use Speckle?

-   **Built for AEC**\
    Speckle gets the complexity of AEC data. It handles geometry, metadata, version history, and relationships between elements, all without flattening or losing meaning.

-   **Makes data exchange look easy**\
    Speckle connects your favorite tools; like Revit, Rhino, Power BI, Grasshopper, SketchUp, Blender, AutoCAD, Archicad and more, so you can send and receive model data without skipping a beat.

-   **Teamwork online**\
    Speckle brings your models to life on the web, making it easy to share, view, and discuss—no special software or plugins needed.

-   **Open, flexible, and extensible**\
    Speckle is fully open source. Use it as-is, extend it to fit your workflow, or build custom apps and automations on top of it. It’s designed to grow with your needs.

## How Speckle Works

Speckle works without files to unlock your models from proprietary formats and desktop files.

To do this, Speckle relies on a set of integrations, called **connectors**. These are lightweight plugins that integrate directly into the software you already use, such as: Revit, Rhino & Grasshopper, Blender, etc.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/introduction/intro-speckle-1.jpg" alt="connector-data" />
</Frame>

Connectors publish your models to Speckle without relying on files—every piece of geometry or metadata is extracted and uploaded. Once your models are published to Speckle, they are stored securely in our cloud.

Speckle also supports drag & drop file uploads for formats like IFC, OBJ and STL directly in the web app.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/introduction/intro-speckle-2.jpg" alt="connectors" />
</Frame>

Speckle models are not only securely stored and versioned in our cloud, they can be consumed in a variety of ways:

-   Load them back inside other apps (for example Revit or Power BI), via the connectors. Again, no file exports needed!
-   View and share them from the Speckle web app and our powerful online 3D viewer (for example by embedding them in a Miro board, or sharing a link to your coworkers).
-   Take your models further into custom apps you can develop thanks to Speckle's Developer Platform.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/introduction/intro-speckle-3.jpg" alt="web_app_dev_platform" />
</Frame>

## What You Can Do With Speckle

-   **Exchange designs**\
    Iterate faster by exchanging data between disciplines. Share only what's needed and coordinate in real time.

-   **Get insights**\
    Leverage the Power BI connector to create interactive dashboards that consume BIM and AEC data for stakeholders.

-   **Present & review models**\
    Use the online 3D viewer to share interactive models via link or embed. Perfect for reviews with version history, follow mode, federation, and 3D comments.

    It's perfect for model reviews too, with features like version history, real-time follow mode, model federation, and 3D comments pinned to objects.

-   **Build custom tools**\
    Access building blocks for developing custom apps, integrations, and automations - no need to start from scratch.

-   **Store & future-proof**\
    Keep all your designs in a secure, transparent cloud. You own your data - our platform just hosts it.

## Next Steps

1. **Get started**: Head to the [Quickstart guide](/quickstart/quickstart) to set up your first workspace and project.
2. **Find answers**: Browse the [Frequently asked questions](/quickstart/faq) for common issues and tips.
3. **Explore tutorials**: Visit our [Tutorials page](https://speckle.systems/tutorials) for workflow examples.

Welcome aboard; let's dive in and see what Speckle can do!

# Billing

Source: https://docs.speckle.systems/workspaces/billing

Information about managing your paid subscription

<Note>Workspaces come in three plans: **Free**, **Starter**, and **Business**. View pricing and find the plan that matches your needs on [speckle.systems/pricing](https://www.speckle.systems/pricing). Speckle is free without limits for academia.</Note>

## Subscribe to a Plan

Upgrade your workspace to one of the paid plans under Settings -> Billing.

-   We support both monthly and annual payment options.
-   Charges happen towards a payment card that you connect to your active subscription.
-   Paying via invoice is reserved for contracts above a certain usage limit and only for annual subscriptions. Contact us if you are interested in this.

## Paid Versus Free Seats

You pay for users who are assigned an Editor seat. Users on Viewer seats are always free. Learn about the difference [here](/workspaces/roles-and-seats#seats).

## Buy and Remove Seats

Subscription costs adjust dynamically as `Admins` assign and remove Editor seats from workspace users. You can buy, assign, and remove seats under Settings -> People.

-   **Buy Editor seats:** If you want to buy an Editor seat, go to the user who needs the seat under Settings -> People and upgrade their seat from Viewer to Editor. This will immediately increase the subscription cost by one seat unless an unused Editor seat was available.

-   **Remove Editor seats**: Removing an Editor seat from a workspace user does not immediately lower the subscription cost. The Editor seat remains billed and available until the next billing cycle begins.

-   **When someone leaves a workspace:** When a user on an Editor seat leaves your workspace, their Editor seat remains billed and available until the next billing cycle begins.

-   **Billable seats are automatically adjusted:** The number of Editor seats you are billed for is automatically adjusted when a new billing cycle starts. Example: You pay for 5 Editors seats and remove an Editor seat from a user without reassigning it to someone else. -> Your subscription will be downgraded to 4 Editor seats when the next billing cycle starts.

## Change Your Subscription

You can make changes to your subscription under Settings -> Billing.

-   **Change billing cycle:** Change from a monthly to yearly billing cycle to save 10% on your subscription costs. It's not yet possible to change from a yearly to a monthly billing cycle without cancelling your subscribtion and resubscribing.

-   **Get unlimited projects and models:** You can add the _Unlimited projects and models_ add-on to your Starter or Business plan to remove those usage limits.

-   **Upgrade plan:** Easily switch to a higher-tier plan as your needs evolve.

-   **Downgrade plan:** This is not yet supported via the app so please contact us if you wish to downgrade to a lower-tier plan.

-   **Cancel plan:** You can cancel your subscription to stop future charges. The subscription will remain active until the end of the current billing cycle. When cancelled, your data will remain intact and available, but the workspace is in a read-only mode.

# Data Residency

Source: https://docs.speckle.systems/workspaces/data-residency

Choose where your data is stored for compliance

<Note>
  Data residency is available on the Business plan.
</Note>

Data residency means storing your data in a specific geographic location to meet local laws and regulations.

## Why does data residency matter?

Different regions have different requirements for where data can be stored:

-   GDPR requires that EU citizens' personal data is protected according to European standards, no matter where it's stored or processed.
-   Some government organizations in countries like Australia must keep certain data within their borders.

By choosing where your data is stored, you can meet these requirements and demonstrate compliance.

## How does data residency work in Speckle?

Speckle workspaces let you choose where your data lives, so you can stay compliant while keeping full control over your data.

-   Every workspace starts in Speckle's default region.
-   Business plan customers can choose a different region for their workspace to meet their compliance needs.
-   The **Extra data region** add-on lets you set data residency at the project level for more granular control.

## Available Regions

Data residency is available on the Business plan.

-   Choose from **EU**, **UK**, **North America**, or **Asia Pacific** as your workspace's default region. All of your project data will be stored in this region.
-   For more granular regions, and project-specific regions, <a href="mailto:billing@speckle.systems">
    contact us</a>

    about the **Extra data region add-on**.

-   If you don't specify a region, your data automatically goes to Speckle's default region, optimized for performance and speed.

# Domain Discoverability

Source: https://docs.speckle.systems/workspaces/domain-discoverability

Make it easy for your coworkers to join

### How does domain discoverability work?

Domain discoverability provides a low-friction way to allow coworkers to join your workspace.

When enabled, new Speckle users signing up with your verified email domains will be prompted to join your workspace. They can **request to join**, which triggers an email notification to all Admins. Request can then be accepted or rejected from the _Join requests_ page under Workspace Settings -> People.

If you reject someone's join request, they won't be able to request to join again. However, you can still invite them manually.

We recommend enabling domain discoverability to help more of your coworkers end up in the same workspace instead of creating separate ones. This also reduces the need for manual invites.

<Info>Domain discoverability doesn't prevent your coworkers from creating other workspaces. It only encourages joining the same one. Completely preventing other workspaces from being created is an Enterprise feature.</Info>

### How do you enable domain discoverability?

Admins can enable domain discoverability under Workspace Settings -> Security.

<Steps>
  <Step title="Connect verified domains to workspace">
    Domain discoverability works by connecting one or more verified domains to the workspace. Add these from the top of the Security settings page.

    The email domain you used when signing up to Speckle will already be verified, so you can add it as a verified domain to your workspace with a single click (unless you signed up with Gmail, Outlook, or another standard email provider).

    To connect additional domains to your workspace, first verify more emails in your [email settings](https://app.speckle.systems/settings/user/emails). Any emails you verify there will show up as available domains you can connect to your workspace.

  </Step>

  <Step title="Enable domain discoverability">
    Enable domain discoverability with the toggle switch on the Security settings page.
  </Step>
</Steps>

### Joining without admin approval

When a user discovers your workspace, you can decide if they should **request to join** (followed by admin approval), or **join immediately without admin approval**. You can enable instant joining from the same place you enable domain discoverability.

<Warning>
  Joining without admin approval should be used with caution. Suitable for **Enterprise** and **Academia** plans else you would be at risk of an uncontrolled escalation of your billing.
</Warning>

# Domain Protection

Source: https://docs.speckle.systems/workspaces/domain-protection

Secure who can access your workspace

<Note>
  Domain protection is available on the Business plan.
</Note>

Domain protection lets you control who can access your workspace by limiting it to users with specific email domains.

### How do you enable domain protection?

Admins can enable domain protection under Workspace Settings -> Security.

<Steps>
  <Step title="Connect verified domains to workspace">
    Domain protection works by connecting one or more verified domains to the workspace. Add these from the top of the Security settings page.

    The email domain you used when signing up to Speckle will already be verified, so you can add it as a verified domain to your workspace with a single click (unless you signed up with Gmail, Outlook, or another standard email provider).

    To connect additional domains to your workspace, first verify more emails in your [email settings](https://app.speckle.systems/settings/user/emails). Any emails you verify there will show up as available domains you can connect to your workspace.

  </Step>

  <Step title="Enable domain protection">
    Enable domain protection with the toggle switch on the Security settings page.
  </Step>
</Steps>

<Info>
  If your organization uses the [SSO](/workspaces/sso) feature, you don't need to also enable domain protection.
</Info>

### When domain protection is enabled

1. Admins cannot invite new members whose email isn't from the verified domains list.
2. Users with the Guest role can still join the workspace even if their email doesn't match any verified domains, since this role is designed for external collaborators.

# Invite to Workspace

Source: https://docs.speckle.systems/workspaces/inviting

Information about workspace and project invites

### How to invite to your workspace?

Admins can invite new users to a workspace under Workspace settings -> People.

When inviting, you need to decide if someone should join the workspace as a Member or a Guest. The Member role is meant for coworkers, while the Guest role is meant for external collaborators. You can learn more about Members and Guests [here](/workspaces/roles-and-seats#workspace-roles).

By default, new users are assigned the free Viewer seat when they are invited to a workspace. This means they won't be able to contribute to projects as an editor until an Admin has upgraded their seat to an Editor seat. You can learn about seats [here](/workspaces/roles-and-seats#seats).

### Bulk Inviting

There's a hidden—but smart—feature in the invite modal if you need to invite a lot of users at the same time.

1. Copy a list of emails to your clipboard. The emails can be separated by spaces, commas or semicolons.
2. Paste the emails into the first email input in the invite modal.
3. The emails will now be pasted into individual inputs for easy sending.

### Inviting to a Single Project

If you want someone to have access to just a single project in your workspace—or a select few—then you can invite them to your workspace as a Guest. This role is typically reserved for external collaborators, and it ensures that someone have access to the exact projects you grant them access to. You can learn more about Guests [here](/workspaces/roles-and-seats#workspace-roles).

To send a project invite, navigate directly to the project and send the invite from the Collaborators tab. People invited from here _always_ join the workspace as Guests. If you later want a person to become a full workspace Member then you can update their workspace role from Settings -> People.

# Models

Source: https://docs.speckle.systems/workspaces/models

Organising your data in Speckle

**Models** help you organise your data within a project. They're useful for splitting
different parts of your work, such as design options, disciplines, or team responsibilities.
A model can be a direct relationship to a 3d model file, or a portion of it, or it can related
to multiple files within a single model. Models work best when they are used to represent a
particular part of your work, a focus for a conversation, a single package deliverable
or a particular discipline, the choice is yours.

## Creating Models

A new project starts without models present. You can create an empty model in the web interface or
from a connector. This is simply a container for your data; it will have data in it
once you publish data from a supported design tool using a connector.

You can keep everything in that model or create additional ones to explore design options,
separate work by team or discipline, and organise project components more clearly.

Models give you the flexibility to structure your data to fit how you work.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/mode-folder-structure.jpg" />
</Frame>

## Managing Models

You can create as many models as you need within a project within your workspace limits.
The Speckle Web App makes it simple to add new models and switch between them.

Models can be named to mimic a folder structure by using a forward slash `/` in the name,
e.g. `Building A/Floors/Floor 1`.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/mode-folder-create.jpg" />
</Frame>

## Frequently Asked Questions

<AccordionGroup>
  <Accordion title="Can I choose who can edit specific models?">
    No, edit rights are set at the project level only at this time.
  </Accordion>

  <Accordion title="Can I set a model as read-only?">
    No, read-only status is set at the project level only at this time.
  </Accordion>

  <Accordion title="Why use multiple models?">
    Here are a few common reasons:

    * **Split by discipline**: For large projects, separate models by team, e.g., <em>Architecture</em>, <em>Structural</em>, and <em>MEP</em>. This ensures each team receives only what’s relevant.
    * **Split by building**: If your project includes multiple buildings, keep them in one project but create separate models like <em>Building A</em>, <em>Building B</em>, and <em>Building C</em>.
    * **Explore design options**: Want to present different façade concepts? Create models like <em>Option A</em>, <em>Option B</em>, and <em>Option C</em> and switch between them to show your client.

  </Accordion>

  <Accordion title="What does 'federating models' mean?">
    In Speckle, you can <strong>federate models</strong> by loading multiple models into the same view — even if created separately.
    This is useful for working with different teams or disciplines. For example, view the <em>architecture</em>, <em>structure</em>, and <em>MEP</em> models together in a single, coordinated view without merging them into one file.

    Federating models helps you:

    * Compare design options
    * Coordinate between disciplines
    * Keep models separate while viewing them side by side
      You can do this directly in the <strong>Speckle 3D viewer</strong> or in supported
      design tools using our **connectors**.

  </Accordion>

  <Accordion title="How do I create and manage models?">
    You can create as many models as needed within a project. The Speckle Web App makes it simple to:

    * Add new models
    * Rename models
    * Switch between models
      This helps you keep your work organised and ensures each model is used as intended.

  </Accordion>

  <Accordion title="How do I delete a model?">
    You can delete a model by selecting the **Delete model** button in the model settings drop-down found on the models list page.
    This will remove the model from the project and **all associated data**.
  </Accordion>

  <Accordion title="How many models can I have in a project?">
    You can have as many models as you need in a project. However, the number of models you have in total in your workspace
    across all projects may be limited by your workspace plan.
  </Accordion>

  <Accordion title="How do I switch between models?">
    You can switch between models by selecting the model from the models list page.
    This will open the model in the Speckle Web Viewer.
  </Accordion>

  <Accordion title="Can I rename a model?">
    Yes, you can rename a model by selecting the model from the models list page and clicking the **Rename model** button.
  </Accordion>

  <Accordion title="How do I move a model to another folder?">
    You can move a model to another folder by selecting the model from the models list
    page and clicking the **Rename model** button.
    It is the presence of `/`s in the model name that determines the folder structure.
  </Accordion>

  <Accordion title="How many folders can I have?">
    You can have as many folders as you need in a project. It is the presence of `/`s in the
    model name that determines the folder structure. However, it may be preferable to only use
    one or two levels of folders to keep your models organised.
  </Accordion>

  <Accordion title="Is there a maximum size for a model?">
    Theoretically no, but the performance of the 3D viewer will be impacted if it is large number of
    extremelly detailed objects. It can be benefical to break models up and federate them together
    as required to keep the performance high.
  </Accordion>
</AccordionGroup>

# Projects

Source: https://docs.speckle.systems/workspaces/projects

Organising your data in Speckle

## What are projects?

In Speckle, a **project** is where your data lives.

Think of a project as a container that helps you organise, manage, and share your work. You can give each project a name and description to help you keep things clear and easy to find.

Projects also let you **collaborate** with others. You can share a project with your team and control who can view or edit it.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/project-start.jpg" />
</Frame>

## What can a project contain?

A project can hold anything—from a few objects to an entire building model. You can create as many projects as you like and add as much (or as little) data as you need.

Some examples of what a project might include:

-   A layer from a CAD application
-   A furniture (Revit family)
-   A workset or selection from Revit
-   A group of objects from Grasshopper
-   A structural model
-   Calculation results

Projects are containers for **models** and **versions**, no project design data lives outside of a model version.
We'll explain how those work in the next sections. Only the name and description and
the members of a project exist outside of a model version.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/project-overview.jpg" />
</Frame>

## Who can I share projects with?

While a workspace can have **members** and **guests** that can impact who can have access to the
projects within it, projects themselves can be shared with specific users to control access and
within the security settings of the workspace.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/project-access.jpg" />
</Frame>

### Access Control

A project can have a global state of:

-   **Public**: Anyone with the link can view,
-   **Workspace**: All workspace members can view, but not guests, or
-   **Private**: Only for project members and admins.

### Discussions

The ability to contribute to discussions is controlled at the project level:

-   **Anyone**: Anyone can contribute to discussions with comments and replies if they have access to the project and have a Speckle account.
-   **Collaborators**: Only project collaborators can contribute to discussions.

Learn more about discussions in the [discussions](/3d-viewer/discussions) page.

## Frequently Asked Questions

<AccordionGroup>
  <Accordion title="Is there a limit to the number of projects I can create?">
    The number of projects you can create is subject only to the limits of your workspace.
  </Accordion>

  <Accordion title="Can I delete a project?">
    Yes, you can delete a project by selecting the project from the projects list
    page and clicking the **Delete project** button.

    <Warning>
      Deleting a project is destructive. It will delete all the data associated with it.
    </Warning>

  </Accordion>

  <Accordion title="Can I rename a project?">
    Yes, if you the project owner, you can rename a project by selecting the
    project from the projects list page and clicking the **Rename project**
    button.
  </Accordion>

  <Accordion title="Can I move a project to another workspace?">
    No, not in the web interface, if this is something you need critically,
    contact us either in the application chat or by email at [support@speckle.com](mailto:support@speckle.com) A
    project made in the personal projects era can be migrated one time to a
    workspace.
  </Accordion>

  <Accordion title="If I rename a project will it break anything?">
    No, it will not break anything. The only thing that will be affected is the
    name of the project.
  </Accordion>

  <Accordion title="Can I enforce naming conventions to project names?">
    No, you cannot enforce naming conventions to project names.
  </Accordion>

  <Accordion title="Can I change the description of a project?">
    Yes, you can change the description of a project by selecting the project from
    the projects list page and clicking the **Edit project** button.
  </Accordion>

  <Accordion title="Is there a limit to the number of members in a project?">
    No, there is no limit to the number of members in a project. However, depending on your
    **workspace plan** you may be charged for additional project members not already in your workspace.

    You can add as many **viewers** to your project as you like, they are free.

  </Accordion>
</AccordionGroup>

# Roles and Seats

Source: https://docs.speckle.systems/workspaces/roles-and-seats

Understand the key concepts for managing permissions

This guide explains Speckle's project roles, workspace roles, and seat types. The table below gives you a high-level overview of how these combine to determine what users can do.

<table>
  <thead>
    <tr>
      <th style={{ textAlign: 'left' }}>Workspace role</th>
      <th style={{ textAlign: 'left' }}>Seat</th>
      <th>View & comment</th>
      <th>Publish & load</th>
      <th>Create projects</th>
      <th>Manage workspace</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Admin</td>
      <td><code>Editor</code></td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>
    </tr>

    <tr>
      <td>Member</td>
      <td><code>Editor</code></td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>
    </tr>

    <tr>
      <td>Member</td>
      <td><code>Viewer</code></td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>
    </tr>

    <tr>
      <td>Guest</td>
      <td><code>Editor</code></td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>
    </tr>

    <tr>
      <td>Guest</td>
      <td><code>Viewer</code></td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="check" iconType="solid" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>

      <td style={{ textAlign: 'center' }}>
        <Icon icon="xmark" iconType="solid" color="#dc2626" />
      </td>
    </tr>

  </tbody>
</table>

<Info>Guests can only view, comment, publish and load in the specific projects they are invited to.</Info>

---

# Project Roles

Project roles determine what actions a user can perform within a specific project. `Admins` and `Project owners` can manage the roles from the Collaborators tab on the project page.

<Tabs>
  <Tab title="Project owner">
    * Has full ownership of the project, including inviting new project members, managing project roles, and all project settings.
    * The project creator is automatically the first `Project owner`.
    * Workspace admins have the `Project owner` role on all projects in a workspace, even private projects.
    * An `Editor seat` is required to have the `Project owner` role.
  </Tab>

  <Tab title="Can edit">
    * Can fully contribute to a project including creating new models and versions
    * Can load and publish models from AEC software using the Speckle connectors.
    * An `Editor seat` is required to have the `Can edit` role.
  </Tab>

  <Tab title="Can view">
    * Can view models in the 3D web viewer and add comments.
    * Cannot load models into host apps using the Speckle and publish models from the Speckle connectors.
  </Tab>
</Tabs>

---

# Workspace Roles

Workspace roles determine a user's default project access and workspace-level permissions, like inviting users and managing security settings. `Admins` can manage workspace roles from Workspace Settings -> People.

<Tabs>
  <Tab title="Admin">
    * Full ownership of the workspace, including management of members, projects, and settings.
    * Is automatically `Project owner` of all existing and new projects in the workspace.
    * Cannot be removed or have their role changed within a project.
    * Can create, manage, and oversee all Speckle Automate functions within the workspace.
  </Tab>

  <Tab title="Member">
    * Can access all projects in the workspace with the `Can view` project role, unless the project is set to `Private`.
    * Can create and own projects if assigned an `Editor seat`.
    * Cannot invite new users to the workspace, but can invite existing workspace members to projects.
    * Can access and use Speckle Automate to create private functions.
  </Tab>

  <Tab title="Guest">
    * Role meant for external collabators who only need access to select projects in the workspace.
    * Can hold the `Can edit` project role if assigned an `Editor seat`.
    * Can never create new projects in the workspace.
    * Can never hold the `Project owner` project role.
    * Can join a workspace without adhering to any domain policies or authorizing through SSO.
    * Cannot access or create private Speckle Automate functions.
  </Tab>
</Tabs>

---

# Seats

The seat determines which project roles a user can be assigned. `Admins` can manage seats from Workspace Settings -> People.

<Tabs>
  <Tab title="Editor seat">
    * Gives `Members` and `Guests` permission to fully contribute to projects with the `Can edit` project role.
    * Gives `Members` permission to create new projects in the workspace and become `Project owner`.
    * Is a paid seat on the Starter and Business plans.
    * Is a required seat for `Admins`.
  </Tab>

  <Tab title="Viewer seat">
    * Gives `Members` and `Guests` permission to have the limited `Can view` project role.
    * Is always a free seat.
  </Tab>
</Tabs>

---

# FAQs

**Project roles**

<AccordionGroup>
  <Accordion title="Can non-workspace members have a project role?">
    You can add anyone to a project role if it is allowable by the workspace security settings.
    If a user is added to a project as member who **can edit** they will be added as an editor
    to the workspace. If they are not a member of the workspace they will be added as a guest.
  </Accordion>

  <Accordion title="Can I assign roles to teams?">
    No, roles are set on a member by member basis.
  </Accordion>
</AccordionGroup>

**Workspace roles**

<AccordionGroup>
  <Accordion title="What is a workspace role?">
    A workspace role is a role that determines what actions a user can perform within a workspace.
  </Accordion>

  <Accordion title="What are guest roles?">
    Guest roles are a type of workspace role that allows users to view and comment on models in a workspace.
  </Accordion>

  <Accordion title="How do I invite someone to my workspace?">
    You can invite someone to your workspace by clicking the **Invite** button in the top right corner of the workspace page.

    You can also set your workspace to allow self-signup by making your workspace **domain discoverable**.
    Users with an email domain matching what you have verified to the workspace will be notified your
    workspace exists and can request to join. You can also set it up to automatically add them to the workspace without admin approval.

    <Note>
      Only admins can invite users to a workspace.
    </Note>

    Learn more about [inviting users to a workspace](/workspaces/inviting).

  </Accordion>

  <Accordion title="How do I remove someone from my workspace?">
    You can remove someone from your workspace by clicking the **Remove** button in the top right corner of the workspace page.
  </Accordion>
</AccordionGroup>

**Seats**

<AccordionGroup>
  <Accordion title="Can I swap seats between people?">
    Yes, within a billing cycle if a seat is removed from a workspace member or guest
    then it can be allocated to another.
    <Warning>Allocating a seat to a new member or guest without first unallocating will
    add a prorated cost for an additional seat for that billing cycle.</Warning>
  </Accordion>

  <Accordion title="What happens if I remove an editor seat from a user who is a project collaborator?">
    They will remain a project team member but their role will be downgraded to **can view**.
  </Accordion>

  <Accordion title="What happens if I remove an editor seat from a user who is a workspace member?">
    They will remain a workspace member but their role will be downgraded to **can view**. Their role
    on any projects they are a member of will also be downgraded to **can view**.
  </Accordion>
</AccordionGroup>

# Single Sign-On (SSO)

Source: https://docs.speckle.systems/workspaces/sso

Secure who can access your workspace

<Note>
  SSO is available on the Business plan.
</Note>

Single Sign-On (SSO) allows users to access Speckle using your organization's existing identity provider. Speckle supports any OIDC identity provider.

### How do you enable SSO?

Admins can enable SSO under Workspace Settings → Security.

<Info>
  Need help setting up SSO? We're happy to jump on a call to walk you through the process. [Contact us](mailto:support@speckle.systems) to schedule a meeting.
</Info>

<Steps>
  <Step title="Create an OpenID Connect application">
    Set up a new web application using the OpenID Connect protocol in your identity provider's panel. This will generate the necessary settings for Speckle.

    When configuring the application, use this **Redirect URL** (callback):

    ```
      https://app.speckle.systems/api/v1/workspaces/{workspace-short-id}/sso/oidc/callback
    ```

    The value of `workspace-short-id` should be your workspace's unique short id.

    Set the application grant type to "authorization\_code" and configure these scopes:

    | Scope   | Resultant claims                |
    | ------- | ------------------------------- |
    | openid  | -                               |
    | profile | name, given\_name, family\_name |
    | email   | email                           |

    <Warning>
      You may need to explicitly configure your identity provider to provide user emails with the `email` claim. Some providers, like Azure AD, will omit or obscure this information by default.
    </Warning>

  </Step>

  <Step title="Configure SSO in Speckle">
    Fill in the SSO configuration form with details from your identity provider:

    * **Provider**: The label displayed on the login button in Speckle
    * **Client ID**: From your identity provider application
    * **Client secret**: From your identity provider application
    * **Issuer URL**: Your identity provider's issuer URL

  </Step>

  <Step title="Enable SSO">
    Click **Add** to save your SSO configuration. Once SSO is enabled, all workspace members will be required to authenticate with SSO credentials the next time they access the workspace.
  </Step>
</Steps>

### When SSO is enabled

1. Users will see your organization's SSO option when they are invited to the workspace.
2. Existing workspace members will be prompted to authenticate with SSO the next time they access the workspace.
3. Users with the Guest role can still access the workspace without SSO, since this role is designed for external collaborators.

<Warning>
  SSO provides authentication but not automatic user provisioning. Users removed from your identity provider will still be in your list of members in Speckle until a Admin in Speckle has removed them.
</Warning>

<Info>
  If your organization uses SSO, you don't need to enable [domain protection](/workspaces/domain-protection) as SSO provides equivalent security controls.
</Info>

# Version Control

Source: https://docs.speckle.systems/workspaces/versions

Keep track of every model

Every time new data is published to a **model**, a new **version** is created.
This is a snapshot of your model at a specific point in time, a moment in your project's history.
Versions are store forever or until you delete a model for which they were created.

Versions help you keep track of changes, they record who published them, form which source
updated what and when, by default eveyone always sees the latest version with the flexibility
to go back to a previous state if needed.

Each version includes:

-   All the objects in your model
-   The date and time it was created
-   The person who published it
-   (Optional) A short message describing what changed

This makes collaboration easier, keeps your work organized, and ensures nothing gets lost along the way.

## How do I use versions?

If you've sent data through a **connector**, you've already used versions, they're
created automatically each time you publish to a project.

Once you've published a new version, to keep things clear you can add a **version message**:
a short note that explains what the version includes. This is optional, some connectors
will suggest a default message for you, but you can decide when a versions should have a special status.

### Receiving Version Data

When **receiving data**, you can choose to:

-   Stay synced with the **latest version**, or
-   Load a **specific version** using its version ID

If you're synced with the latest version, you'll get a notification when someone
sends new data to the project. You can then click **Receive** to bring in the latest
updates and keep your file current.

### Accessing and Editing a Version

You can view and manage all versions of your model directly from your project space.

There are two main actions you can take on a version:

-   **Edit the version message**
-   **Delete the version**

To do this:

1. Click the three dots next to the model.
2. Select **View versions**.
3. Find the version you want to update and click the three dots in the top-right corner.
4. Choose **Edit message** or **Delete version**.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/version-access.jpg" />
</Frame>

<br />

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/version-settings.jpg" />
</Frame>

### Latest Version

The latest version is always the default, but you can delete that version which will
promote the immediately previous version to be the latest. Alternatively you can simply
publish a new version which will become the latest.

### Comparing Versions

Because all versions are kept and cannot be changed once published you can compare
two versions to see the differences between them. This is useful to review changes,
or to see what changed between two specific points in time. More info about [Comparing Versions](/3d-viewer/compare-versions).

## Frequently Asked Questions

<AccordionGroup>
  <Accordion title="Can I set an approval status on a version?">
    You can only set the version message, potentially to something meaningful like "Approved for release".
  </Accordion>

  <Accordion title="How long are versions stored for?">
    Versions are stored indefinitely, but you may be limited as to how many you can see depending on your workspace plan.
  </Accordion>

  <Accordion title="Can I prevent others from seeing specific versions?">
    No, once a version is published it is visible to all users with permission to view the model.
  </Accordion>

  <Accordion title="Can I prevent others from deleting versions?">
    Only the owner of the model can delete versions.
  </Accordion>

  <Accordion title="How many versions can I publish?">
    You can publish as many versions as you want, but you may be limited as to how many you can see.
  </Accordion>

  <Accordion title="I already published a version, can I still set or edit its version message?">
    Yes, you can set or edit the version message for any version from the version history page.
  </Accordion>

  <Accordion title="I can't see older versions">
    All older versions are stored indefinitely but may be hidden if depending on your workspace plan limits.
  </Accordion>

  <Accordion title="How do I visually compare versions?">
    You can compare two versions to see the differences between them. This is useful to review changes,
    or to see what changed between two specific points in time. You can do this in the 3D viewer, more details
    can be found in the [compare versions](/3d-viewer/compare-versions) page.
  </Accordion>

  <Accordion title="How do I delete a version?">
    If you've published a version by mistake you can delete it. This will remove it from the model
    and if you delete the latest version it will make the previous version the latest.
  </Accordion>

  <Accordion title="How do I restore a version?">
    You can't promote a specific version to be the latest, but you can publish a new version
    which will become the latest. Or delete all newer versions. Receiving a specific
    version and re-publishing it will theoretically restore it, but this can be a lossy
    process depending on the connector. More reliable would be to do so programmatically.
  </Accordion>

  <Accordion title="How do I set a version message?">
    You will prompted in your connector to set a version message when you publish.
  </Accordion>
</AccordionGroup>

# Overview

Source: https://docs.speckle.systems/workspaces/workspaces

Workspaces act as a secure hub for your team and projects using Speckle.

## What is a Workspace?

A workspace is an organizational structure for your teams’ projects and models.
It provides a secure, centralized environment for managing roles, permissions, and data access.
Workspaces are flexible and customizable, with optional plans and add-ons to meet your needs.

### Organization

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/speckle/images/workspaces/workspace-overview.jpg" />
</Frame>

## Key Features of Workspaces

Workspaces are designed to:

-   Enable granular access control for projects and team members.
-   Provide domain-based membership protection for enhanced security.
-   Support team collaboration with centralized project and user management.
-   Streamline workflows and data sharing.
-   Allow for collaborative development of automations with Speckle Automate.
-   Offer flexible plans with advanced features like Single Sign-On (SSO) and custom data residency.

## Workspace Plans

Speckle offers workspace plans to fit every need:

-   Small teams with many projects and models.
-   Organizations needing data residency within specific territories.
-   Enterprises managing large numbers of users and projects.

For an up-to-date list of plans and features, visit [our main website](https://www.speckle.systems/pricing).

## Explore Further

Use the sidebar to learn more about managing projects, inviting users, setting roles,
and ensuring data security in your workspace.
