---
created: 2025-03-26 20:20:10
update: 2025-04-13 21:29:10
publish: false
tags: 
title: 
description: 
authors:
---

# A community based, wiki-like space for sharing knowledge

started 18. 01. 2025
https://nica-ev.github.io/docs/
https://nica.network

## why ?
- through the erasmus+ projects i realized how much knowledge is out there that isnt easy accessible
- information is spread all over the place, often only receivable through personal connections
- i have also seen multiple times how spaces that started such an effort (i.e. Social Circus Resources, European Juggling Magazine) went away and with them an easy access to this information
	- this is something we want to avoid by design

## core idea: 
- having a space to share information about movement based pedagogy and similar topics
- this space should not be dependend on a single person or society
- it should be not reliant on specific software if possible (altough specific software might make working with it easier)
- overall, the content should be seperated from the visualisation
	- this helps with accessibility down the line
- every content should be free to use for whatever, but should still be kinda protected against misuse
	- CC-BY-SA 4.0 license (Creative commons, by attribution, sharealike)
	- https://creativecommons.org/licenses/by-sa/4.0/deed.en

## further
- it should be possible to automatically translate into any (major) language to remove language barriers
- it should be possible to visualize / consume the content in different ways (websites, apps, printed version, the pure content files etc.)

## Current Design / Implementation
- wiki like setup (mostly text and images, linked and searchable)
- use of metadata to enhance discoverability
- markdown based (a widely used text standard that allows basic formating, is human readable and independend of specific software)
- a version control system (Git, Open Source) that allows for full transparency about any changes to the content
- Github (Microsoft - but lots of alternatives exist) for online, community based work
	- while Github isnt OpenSource, its a widespread and very stable service that literally millions of open-source projects use (mainly IT, software)
- while the original project is obviously tied to a single person, it can be copied (forked) and used by others to its full extend
- Visualization of the content is currently done by using another OpenSource Project (MkDocs, MkDocs Materials) that builds a static website (wich is currently hosted by Github Pages, wich for public projects is free)
	- This is a proven setup that is used by thousends of companys (even very big ones) for project-documentation
	- https://squidfunk.github.io/mkdocs-material/
- It would be entirely possible to use the content (or parts of it) to display in an app, print as a book, use offline etc. 

## What is working, whats not right now
- the core systems are working
- Translation is in the works (but more tricky than it initially looks) - but NOT working right now (but its a super high priority)
- Translation itself is costly (the current content, translated by DeepL into one other language would roughly cost 40.- €) - in the long run we have to think about a donation system, so far we cover all expenses from our society
- Right now there are 170 pedagogy based game descriptions, documentation of our society

## How to make sure that the project doesnt die in a year
- we use the system right now as a resource for our society (documentation on process we use, aswell as pedagogy resources)
- this means we have (atleast for the coming years) a clear incentive to keep this project going
- we started talking with people about it personally (youth centres, schools etc.) that might use the information
- slowly inviting people to participate - this can be a slow process (there is an initial hurdle)
- recognizing barriers (technical barriers aswell as motivational ones) and trying to find workarounds or solutions
	- providing easier ways to participate without interacting with the system itself
	- documenting how to use the system (both in text and video)

## Interested ? How to use, participate or contribute
### using it
- easiest thing: just use the website to get information
- download the repository to just use it offline in its most simple form

### contributing
- send things by email, letter, photo or whatever
	- wiki@nica.network
- use github to contribute directly (we can help with getting this to work for you)

---
![[abhuva_Minimalist_line_drawing_of_three_figures_in_motion_formi_d579b82a-1129-4eea-859f-a79b58849010.png]]
# **An Open, Community driven Knowledge Space**

## **1. Introduction (2 minutes)**

- In my work within Erasmus+ projects and in our society, I've consistently been struck by the wealth of knowledge in movement pedagogy. 
- But I've also noticed how often this knowledge feels scattered and difficult to access.
- This observation led me to think about how we could create a more accessible and sustainable way to share this collective wisdom.  Not just for ourselves, but for the broader community.
- This is what sparked the idea for this project.  It's an initiative – still very much in early development – to build a community-based knowledge space for movement pedagogy.
![[abhuva_Minimalist_illustration_of_a_fading_book_dissolving_into_85d1142f-719f-404e-9369-4075621ea158.png]]
## **2. The "Why" - Problem & *Underlying Motivation* (4 minutes)**

- I'm sure many of you have experienced this: you remember a great game from a workshop, or you know there's a fantastic resource out there, but you can't quite put your finger on it. 
- Or you've seen valuable online **resources disappear** over time.

* This frustration was a key driver for this project.  We wanted to address not just the **accessibility** of knowledge, but also its **sustainability**.  
* We've seen too many valuable resources become inaccessible because they were tied to a single person or organization.

**The core idea**
- So, the core idea is simple: to create a shared, open space where we can collectively document and share information about movement pedagogy (and similar topics).  
- A kind of community-built library, if you will - thats owned by the community, not an individual (or society)

![[abhuva_Minimalist_illustration_the_Creative_Commons_CC-BY-SA_ic_701978df-88c4-4768-afad-6f435ae5dde6.png]]
## **3. *Design Principles* (5 minutes)**

* **Open & Wiki-like** 
	* We opted for a wiki-like structure because it's inherently open and collaborative.  It's designed to be easily contributed to by many people, not just a select few.  And the focus on text and images makes it accessible and relatively simple to use.

- **Plain Text**
	- We chose to use Markdown, a plain text format, for the content.  This might sound a bit technical, but the reason is simple: plain text is incredibly durable and independent of specific software.  It ensures that the content remains readable and usable even if technology changes in the future.  It's about long-term **sustainability** and **portability** of the information.

* **Transparency & Community Ownership**
	* We're using a version control system called Git, hosted on GitHub.  
	* Again, this might sound technical, but the core idea is **transparency**.  
	* Git tracks every change made to the content, making the entire history of the project visible to everyone.  This transparency is crucial for building trust and fostering community ownership.  It also allows others to easily 'fork' or copy the project and adapt it for their own needs, further **decentralizing** it.

* **Content/Visualization Separation
	* We've intentionally separated the content itself from how it's displayed.  
	* This means the same content can be used to generate a website, but also potentially an app, a printed book, or other formats in the future.  This flexibility is important for **accessibility** and **adapting** to different needs.
	
* **Openness & Ethical Use** 
	* We've chosen the Creative Commons **CC-BY-SA** license.  
	* This means the content is free for anyone to use and share, but with attribution and share-alike conditions. 
	* It's about ensuring open access while also protecting the integrity of the resource and encouraging further sharing within the community.

![[abhuva_Simple_geometric_shapes_forming_a_structure_representing_20bfee81-287f-49ba-b3d9-9530920cb166.png]]
## **4. Invitation to Explore, Contribute (3 minutes)**

* At this stage, the project is very much a work in progress.  
* We have a working prototype with a growing amount of content – currently around 200+ notes on pedagogy and games, plus documentation for our own society.
* Translation isnt available yet - but its high priority, till then the inbuild Google Translate from most browsers works flawless on the site

* **Exploration and feedback** 
	* "We'd love for you to explore the website nica-ev.github.io/docs and see what's there.  
	* We're particularly interested in your feedback.  Does this kind of resource seem useful?  Are there things that are missing or could be improved? 
	* We are at the start of the project and we all can shape how it will grow

* **Contribution** 
	* If you're interested in contributing, there are many ways to do so.  
	* The easiest is simply to share your ideas, games, or resources with us via email [wiki@nica.network].  
	* We can then integrate them into the platform.  
	* For those who are more technically inclined, there are also ways to contribute directly through GitHub, and we're happy to provide guidance.

* **Collaboration** 
	* This is intended to be a community resource, and its **development will be shaped by the community**.  
	* Your feedback and contributions are essential to making it truly valuable and sustainable.

![[abhuva_Minimalist_illustration_of_an_open_doorway_leading_to_a__e24f29f5-9dfc-4b28-b25a-6c924b41290f.png]]
## **5. Q&A  (1 minute)**
- We're really keen to hear your thoughts and suggestions.
- www.nica.network
- https://nica-ev.github.io/

