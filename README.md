# super-weak
MSc thesis William Bos. Considers the weak supervision of Dutch corpora for the purpose of creating more training data for fine-tuning PLMs on Dutch NER. 

### How to use
clone this repo... `git clone https://github.com/Amsterdam-Internships/super-weak/edit/main/README.md`

install requirements `pip install -r requirements.txt` 

open my nb in jupyter lab `jupyter-lab`

important to do it in jupyter lab. jupyter notebook won't work properly

### TODO
![pipeline](https://user-images.githubusercontent.com/33165624/115394487-1a8c9100-a1e3-11eb-9e82-5a6b377a3395.png)

### External knowledge bases <-- currently here 
Establish extensive list of external knowledge bases. Heuristics, classifiers, gazzeteers. 

knowledge base | source
---------------|-------
Frog | [repo](https://github.com/proycon/python-frog)
Polyglot | [pypi.org](https://pypi.org/project/polyglot/)


### Labelling functions
Encode external knowledge bases from list established in previous section in Python. Utilize [skweak](https://github.com/NorskRegnesentral/skweak) package for this. 

### Train the HMM
Again, utilize skweak library for this. Aggregate the labelling functions. 

### Label Dutch text corpus
Current candidate for corpus is [Wablieft](https://taalmaterialen.ivdnt.org/download/tstc-wablieft-corpus-1-2/). 
Pros:
- already got it, easy access
- Dutch newspapers, just like CoNLL-2002

Cons:
- documents probably won't look like the city dataset documents
- "easy language" potentially not representative of either CoNLL-2002 or city data

Utilize HMM model constructed in previous section for the purpose of labelling this text corpus. 

### Fine tuning XLM-R
Freeze parameters and attach final linear layer for the purpose of classifying NER tokens, fine tune using both ConLL-2002 training set and newly acquired weak labelled set. 

### Evaluation 
Evaluate fine-tuned XLM-R model on CoNLL-2002 dev set first (validation set) and tweak hyperparameters, then finally evaluate model on CoNLL-2002 test set. 
After doing the scientific benchmarking, get some labels for city data and evaluate model on this data as well. Maybe consider fine-tuning final model on weakly labelled city data too, if time is sufficiently available. 
