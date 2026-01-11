# Theory Answers


## 5. Latent Space Manipulation

**How can you estimate directions in latent space that correspond to semantic 
attributes (e.g., “Blond_Hair” and "Eyeglasses")?**


To estimate these directions, we rely on vector arithmetic under the assumption that semantic attributes are linearly separable in the latent space. The standard method is the Difference of Means:

1. Encode a labeled dataset of images into latent vectors (z).

2. Group the vectors into two sets for a specific attribute: those with the feature (e.g., all "Blond") and those without (e.g., "Not Blond").

3. Compute the Mean (average) vector for both groups: μ positive and μ negative.

4. Subtract the means to find the attribute direction vector v: