# 🌳 *DeepTree* 🌳

Welcome to my GitHub *DeepTree* repository, where you’ll find various Python packages & jupyter notebooks related to our latest project [publication](https://github.com/KristinaUlicna/CellComp "Team website") with the **CellX** team.

### PhD Project 👩‍🔬: Heterogeneity within Cell Populations 🧬

![Single Cell Proliferation and Colony Expansion Heterogeneity](video.png)(https://www.linkedin.com/posts/kristinaulicna_cellcyclecontrol-microscopy-images-activity-6685890976306745344-gNFo "Single Cell Growth Heterogeneity")

### Project Status:

WORK IN PROGRESS (Last update: 2020/07/30).
_Note: this is not the full repository (yet)_. I am currently restructuring my repo, so please bear with me while I do so. Once completed, you will find my code & supplementary [iPython](https://ipython.org/notebook.html "Jupyter Notebooks") notebooks divided into these sections:

- **single_cell_lineages:**
   + observe individual cell lineage tree representations from example time-lapse microscopy movie
   + map the intrinsic heterogeneity of the cell cycle durations & colony expansion capacity by individual clones
   + investigate the structure of stored cell segmentation, classification & tracking data by our `bTrack` pipeline

- **lineage_tree_analysis:**
   + visualise the heterogeneity of cell cycling times on large data scales
   + use our massive data repository to understand how cell cycling is descended across multiple downstream generations
   + exploit visibly heritable cycling patterns in extended cell families in automatically reconstructed, multi-generational, deep lineage trees in a **fully unsupervised** manner

### Prerequisites & Dependencies Installation

All code in the *CellComp* repository is written in Python and has been tested with Python 3.7+ on OS X. Most of the packages require the following additional packages, namely `numpy, scipy, h5py, matplotlib, tqdm`. For convenience, you can just run the following code to install all the dependencies:

`$ pip install -r requirements.txt`


### Authors, Acknowledgments & Credits

The code committed to this repository was written by Kristina Ulicna (see the [LICENSE.md](../LICENSE.md "Kristina's LICENSE.md file") for more details) and sources from our custom-designed `CellTracking` library ([CellTracking on Github](https://github.com/quantumjot/CellTracking "Cell Tracking Repository" )), which was developed for microscopy data analysis by Dr Alan R. Lowe at UCL. For more information see our [CellX group website](http://lowe.cs.ucl.ac.uk/cellx.html "CellX group website").

If you are interested to learn more, please -> ⭐ <- the repository & don't hesitate to contact me directly via [email](mailto:kristina.smith.ulicna@gmail.com "Click to Email Me") or my [LinkedIn](https://www.linkedin.com/in/kristinaulicna/ "Kristina's LinkedIn Profile") or [Twitter](https://twitter.com/KristinaUlicna "Kristina's Twitter Profile") profile.

![Key Words of my PhD project "Word cloud summarising the key words of my PhD project"](wordcloud.png)
