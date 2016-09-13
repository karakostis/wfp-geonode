.. _training_introduction:

============
Introductions
============

WFPGeoNode is the World Food Programme’s corporate web platform for publishing geospatial data and
maps. It brings together mature and stable open-source software under a consistent and easy-to-use
interface allowing non-specialized WFP employees and cooperating partners to easily access geographic
information, share data and create interactive maps.

Data management tools built into WFPGeoNode allow for integrated creation of data, metadata, and
map visualizations. Each dataset in the system can be either shared publicly or restricted to only specific
users. Social features like user profiles, commenting and rating systems allow for the development of a
GIS community within WFP to facilitate the use, management, and quality control of the data that the
GeoNode instance contains.

By integrating the type of collaboration typically found in social networks with specialized geospatial
tools, WFPGeoNode is designed to easily explore, process, style, and share maps and geospatial data
with other users. It is also possible to upload and make content available via standard OGC protocols
such as Web Map Service (WMS) and Web Feature Service (WFS).

WFPGeoNode is also designed to be a flexible platform that software developers can extend, modify or
integrate to meet their own requirements. Subsequently, any suggestions for improving the platform or
specifying certain needs may be sent to omep.gis@wfp.org.

The **WFPGeoNode User Training Manual** is a comprehensive guide which, together with the Exercise
Data, constitutes a training package designed to build the capacity of WFP staff, partner agencies, and
governmental partners at various levels. This complete training package has been prepared and designed
by the Geospatial Support Unit (GSU) under the Emergency Preparedness and Response Branch (OMEP).
GSU has been providing support and training to strengthen overall GIS capacity internally and externally
since 2009.

The capacity building activities of GSU is in accordance with the objectives as outlined in the WFP
Strategic Plan 2014 – 2017:

    **Strategic Objective One**: “Save Lives and Protect Livelihoods in Emergencies”, **Goal 3**: “Strengthen
    the capacity of governments and regional organizations and enable the international community to
    prepare for, assess and respond to shocks”, as well as

    **Strategic Objective Three**: “Reduce risk and enable people, communities and countries to meet their
    own food and nutrition needs”, **Goal 3**: “Strengthen the capacity of governments and communities to
    establish, manage and scale up sustainable, effective and equitable food security and nutrition institutions,
    infrastructure and safety-net systems, including systems linked to local agricultural supply chains”.

Training Objectives
===================

The overall aim of the WFPGeoNode Training Package is to increase the understanding and awareness
of the benefits of sharing data and geospatial information through open source web-based systems,
such as GeoNode. Specifically, the purpose of this guide is to provide WFP staff and partners with a
comprehensive manual on how to use WFPGeoNode more effectively and provide practical training on
how to achieve this.

At the end of the two training modules, it is expected that the WFPGeoNode user will be able to:

• Understand basic concepts of using an open source web-based system for sharing geospatial information;

• Use main functions of WFPGeoNode as intended for the benefit of the WFPGeoNode community;

• Produce comprehensive and illustrative maps by using existing data layers or by creating new data layers.

How to use the Manual
=====================

The manual is divided into two training modules with varying levels of difficulty: the Basic User Module
and the Advanced User Module. The basic module concentrates on how to consume and use data,
whereas the advanced module is more focused on how to upload your own data, create comprehensive
and illustrative maps, and share information effectively.

The manual is designed to allow users to acquire both theoretical and practical knowledge in a logical
order. Ideally, the user should read the sections while simultaneously view the explained functions “live”
in the WFPGeoNode system. At the end of each module there is an exercise to be completed using the
complimentary Exercise Data. Here the user will practice his/her skills by following instructions in the
manual and perform actions in the training environment

To quickly gain an understanding on how to navigate and use WFPGeoNode, it is possible to proceed
directly to the exercise sections. However, we recommend that beginners read through the whole manual
and do the exercises in the order they are presented. By reading through the entire manual, the user
will be able to relate the theory and logic of the system with the procedures described in the exercises,
thereby allowing the user to practice what has been studied and effectively consolidate his/her knowledge.

It is also recommended that the user continue with the advanced module after finishing the first module,
since the basic module intends to mainly introduce elementary features of WFPGeoNode and prepare the
user for the next level.

The manual can be used in different types of learning environments. It allows individual users to conduct
the training independently in front of the computer without supervision. It can also be used for supervised
group trainings or during in-depth interactive presentations.

WFPGeoNode is accessible at: `www.geonode.wfp.org <http://geonode.wfp.org/>`_. A dedicated training environment has been created
to allow users to familiarize themselves with the functions explained in the manual and to conduct the
exercises. The training environment is accessible at: `www.training.geonode.wfp.org <http://training.geonode.wfp.org/>`_. Completing the entire
WFPGeoNode Training Package is estimated to take half a day - 1.5 hours for the basic module and 2.5
hours for the advanced module.

Terminology
===========

**Features** – geographical points on a map represented as points, lines or polygons (areas). This geo-
referenced information is associated with one or more attributes.

**Attribute** – Descriptive data often associated to specific features through geographic information
contained in the attribute. An attribute can contain information on for example the estimated population
of a country, where the name of the attribute could be shortened POPEST for easy recognition of what
the values of the attribute actually represents.

**Data values** – the data of a specific attribute e.g. representing the number of an estimated population
or the name of a city.

**Attribute table** – table displaying all the attributes of a specific feature and their associated values

**Vector layer** – data layer representing points, lines and polygons on a map.

**Shapefile** – file format used by WFPGeoNode for uploading a vector layer. It is a digital vector storage format for storing geometric location and associated attribute information, including the four file formats:

* **.shp** - shape format; the feature geometry
* **.shx** - shape index format; a positional index of the feature geometry to allow seeking forwards and backwards quickly
* **.dbf** - attribute format; columnar attributes for each shape
* **.prj** - projection format; the coordinate system and projection information, a plain text file describing the projection of the data

**Raster layer** – data layer comprised of either digital aerial photographs, imagery from satellites, digital
pictures, or even scanned maps. The layer consists of pixels organized into a grid where each cell
contains a value representing information (e.g. temperature).

**GeoTIFF** – file format used by WFPGeoNode to upload a raster layer. It is a public domain metadata
standard that allows additional geo-referenced information to be embedded within a TIFF file. The
additional information includes map projection, coordinate systems, ellipsoids, datum, and other
information necessary to establish the exact spatial reference for the file.

**Style a layer** – to modify the appearance of a layer by using less advanced features (such as symbols
and colors) and more advanced features (such as setting rules for conditions and scales) to visualize
certain data attributes.

GIS Products - Key Aspects to Consider
======================================

When producing a GIS product – a physical map, a data layer or a digital map – it is useful to keep a few
things in mind.

* Who is the audience? Tailor your map and the displayed data layers to the audience you are anticipating will use the map.

* Are all data files properly named according to common naming conventions? By applying proper standards much time and effort will be saved.

* Is the chosen background the most appropriate one? Decide which background indicators are important, and then choose a base layer that best reflects your priorities.

* Are icons visualized at an appropriate scale? Icons that are too large can hamper the visual effect of other important data, and icons that are too small can undermine its importance.
