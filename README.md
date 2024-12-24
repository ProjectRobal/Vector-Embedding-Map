### vector embedding map

A structure that use vector embedding to store data. Thing that I have written for a small project where using vector database like QDrant would be overkill. For faster retrieval it precompute an dot product for every stored vector with reference vector.
When we try to add value with vector and similar vector exits in structure, it will be overwrite by incoming value.