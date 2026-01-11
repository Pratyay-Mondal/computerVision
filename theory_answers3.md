## 5. Latent Space Manipulation

**How did we estimate directions in latent space that correspond to semantic attributes (e.g., “Blond_Hair” and "Eyeglasses")?**

To estimate these directions, we rely on **vector arithmetic** under the assumption that semantic attributes are linearly separable in the latent spaces.

The standard method is the **Differences of Means**:

1.  **Encode** a labeled dataset of images into latent vectors ($z$).
2.  **Group** the vectors into two sets for a specific attribute: those *with* the feature (e.g., all "Blond") and those *without* (e.g., "Not Blond").
3.  **Compute the Mean** (average) vector for both groups: $\mu_{positive}$ and $\mu_{negative}$.
4.  **Subtract** the means to find the attribute direction vector $v$:
    $$v_{attribute} = \mu_{positive} - \mu_{negative}$$

To manipulate a new image, we encoded it to get its latent vector $z$, added this direction vector scaled by a factor $\alpha$, and decode the result:
$$z_{new} = z + \alpha \cdot v_{attribute}$$

This pushes the image representaton along the "Blond" or "Eyeglasses" axis, and adding the feature during reconstruction.
