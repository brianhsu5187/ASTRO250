#!/usr/bin/env python
# coding: utf-8
# %%

# %%
from functools import partial, wraps
from matplotlib import pyplot as plt
import matplotlib.image as img
import numpy as np
from astroquery.sdss import SDSS


# %%
def test(test_func):
    """Decorator to register a test function for a function"""
    def wrapper(func):        
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            result = func(*args, **kwargs)  # Execute the function
            return result  # Return original function result
        
        # Run the test immediately upon redefinition
        test_func(func)

        return wrapped_func
    return wrapper



# %%
def test_delta_y_function(delta_y):
    """
    Show a plot of y vs. t based on their delta_y function
    """
    fig, ax = plt.subplots()
    
    v0 = 10
    t = np.linspace(0, 2, 100)
    
    ax.plot(t, delta_y(t, v0))
    ax.set_ylabel(r"y(t)")
    ax.set_xlabel("t")


# %%
def plot_labels_cmd(labels):
    fig  = plt.figure(figsize=(6,4))
    plt.ylabel('$u-r$', fontsize=12)
    plt.xlabel('$r$ [mag]', fontsize=12)
    plt.ylim([-4,4])
    plt.xlim([8,20])

    for k, v in labels.items():
        if k == 'upper-left':
            plt.text(0.2, 0.8, v, transform=fig.transFigure, fontsize=12)
        elif k == 'upper-right':
            plt.text(0.7, 0.8, v, transform=fig.transFigure, fontsize=12)
        elif k == 'lower-left':
            plt.text(0.2, 0.2, v, transform=fig.transFigure, fontsize=12)
        elif k == 'lower-right':
            plt.text(0.7, 0.2, v, transform=fig.transFigure, fontsize=12)
    
    return fig


# %%
def gal_spectra_fill_in_the_blanks():
    q = 'Question: Examine the amount of light being given of at each wavelength for both galaxies. In which galaxy’s spectrum (1 or 2) do you see a greater contribution from blue light compared to red light, indicating bright O stars and the presence of active star formation?'
    print(q)

    answer = input()
    if answer.strip().lower() in ['galaxy 2', '2', 'galaxy2']:
        print("✅ Correct!")
    else:
        print("❌ Incorrect.")


# %%
def galaxy_images():
    fig, ax = plt.subplots(1,2,figsize=(14,7))
    plt.subplots_adjust(wspace=0.05)
    im1 = img.imread('./NGC1399.jpg')
    im2 = img.imread('./NGC1068.png')

    # show image
    ax[0].imshow(im1, origin='lower')
    ax[1].imshow(im2, origin='lower')
    for a in ax:
        a.set_xticks([])
        a.set_yticks([])
        a.spines['top'].set_visible(False)
        a.spines['right'].set_visible(False)
        a.spines['bottom'].set_visible(False)
        a.spines['left'].set_visible(False)
    ax[0].set_title('Elliptical', fontsize=22)
    ax[1].set_title('Spiral', fontsize=22)
    plt.show()


# %%
def fill_in_the_blanks(blanks_data, full_statement):
    """
    Presents a series of fill-in-the-blank questions and checks the answers.

    Args:
        blanks_data: A list of dictionaries, where each dictionary has 
                     'question' (the text with a placeholder like '______') 
                     and 'answer' (the correct word for the blank).
    Returns:
        None (prints the final score).
    """
    score = 0
    total_questions = len(blanks_data)
    
    for index, item in enumerate(blanks_data):
        question = item['question']
        correct_answer = item['answer']

        # Display the question and get user input
        user_input = input(f"Question {index + 1}: {question} Your answer: ")
        
        # Check if the user's input is correct (case-insensitive)
        if user_input.strip().lower() == correct_answer.lower():
            print("✅ Correct!")
            score += 1
        else:
            print(f"❌ Incorrect. The correct answer was '{correct_answer}'.")
        print("-" * 20) # Separator for readability

    # Print the final score
#         print(f"Nice work! You got {score} out of {total_questions} questions correct.")
    print(full_statement)


# %%
def fill_in_the_blanks_1():
    # The input() function always returns a string, so answers should be strings
    quiz_questions = [
        {
            'question': "For Galaxy 1, the apparent magnitude in the u filter is approximately ______ ('greater than', 'the same as', or 'less than') the apparent magnitude for the r filter.",
            'answer': "less than"
        },
        {
            'question': "For Galaxy 2, the apparent magnitude in the u filter is approximately ______ ('greater than', 'the same as', or 'less than') the apparent magnitude for the r filter.",
            'answer': "the"
        }
    ]
    
    full_statement = '''Galaxy 1 has a higher u-r color index value.\n
Galaxy 2 has a lower u-r color index value.'''

    fill_in_the_blanks(quiz_questions, full_statement)


# %%
def fill_in_the_blanks_2():
    # The input() function always returns a string, so answers should be strings
    quiz_questions = [
        {
            'question': "Galaxy ______ (1/2) has a lower u-r color index value,",
            'answer': "2"
        },
        {
            'question': "which means that this galaxy would appear ______ (bluer/redder).",
            'answer': "bluer"
        },
        {
            'question': "This implies it has many O-type stars and that it ______ (is/isn't) experiencing star formation.",
            'answer': "is"
        }
    ]
    
    full_statement = "Galaxy 2 has a lower u-r color index value, which means that this galaxy would appear bluer. This implies that it has many O-type stars and that it is experiencing star formation"

    fill_in_the_blanks(quiz_questions, full_statement)


# %%
def query_sdss(min_color_index, max_color_index):
    query = f"""
            SELECT TOP 100000 p.u, p.r, s.z, s.class, s.snmedian_u, s.snmedian_r
            FROM PhotoObj AS p
            JOIN SpecObj AS s ON s.bestObjID = p.objID
            AND s.class='GALAXY'
            AND s.snmedian_u > 5.0 AND s.snmedian_r > 5.0 
            AND s.z < 0.05
            AND (p.u-p.r) > {min_color_index} AND (p.u-p.r) < {max_color_index}
            """

    results = SDSS.query_sql(query)
    r = results['r']
    u = results['u']
    
    u_r = u-r
    return u_r, r


# %%
def plot_hist(color):
    fig = plt.figure(figsize=(6,5))
    
    plt.hist(color, bins=100, color='gray')
    plt.tick_params(labelsize=12)
    plt.xlabel('$u-r$', fontsize=14)
    plt.ylabel('Number of Galaxies', fontsize=14)
    
    plt.show()


# %%
def plot_sfr():
    fig, ax = plt.subplots(1,3, figsize=(15,5))

    s1 = np.concatenate((np.random.normal(1, 0.9, 20000), np.random.normal(3., 0.12, 10000)))
    ax[0].hist(s1, bins=100, range=(-1,3.5), color='gray')

    s2 = np.concatenate((np.random.normal(1.5, 0.9, 20000), np.random.normal(-0.5, 0.12, 10000)))
    ax[1].hist(s2, bins=100, range=(-1,3.5), color='gray')

    s3 = np.random.normal(1.3, 0.7, 100000)
    ax[2].hist(s3, bins=100, range=(-1,3.5), color='gray');

    for a in ax:
        a.tick_params(labelsize=12, direction='in')
        a.set_xticks([-1,3.5], ['Low','High'])
        a.set_yticklabels([])
        a.set_xlabel('Star-Formation Rate', fontsize=14)
        a.set_ylabel('Number of Galaxies', fontsize=14)
    ax[0].set_title('A', fontsize=16)
    ax[1].set_title('B', fontsize=16)
    ax[2].set_title('C', fontsize=16)
    plt.show()


# %%
def show_cluster_data(ax=None, *args, **kwargs):
    fig, ax = plt.subplots(1,1,figsize=(7,6))

    plt.hexbin(r,color, bins=10, cmap='gray_r', edgecolors='None', linewidths=None,    
           mincnt=1,          # also helps avoid empty-bin outlines)
           antialiased=False)  # prevents faint rendering seams)
    plt.gca().invert_xaxis()
    plt.ylabel('$u-r$', fontsize=14)
    plt.xlabel('$r$ (mag)', fontsize=14)

    return ax


# %%
def show_cmd_data(r, color, ax=None, *args, **kwargs):
    fig, ax = plt.subplots(1,1,figsize=(6,5))

    ax.hexbin(r,color, bins=100, cmap='gray_r', edgecolors='None', linewidths=None,    
           mincnt=1,          # also helps avoid empty-bin outlines)
           antialiased=False)  # prevents faint rendering seams)
    ax.invert_xaxis()
    ax.set_ylabel('$u-r$', fontsize=14)
    ax.set_xlabel('$r$ (mag)', fontsize=14)
    ax.tick_params(labelsize=12, direction='in')

    return ax


# %%
def write_label(x, y, label, ax, color='red', **kwargs):

    if x in {"CHANGE ME", "X"} or y in {"CHANGE ME", "Y"}:
        return #they still need to replace them

    if isinstance(x, str):
        x = float(x)

    if isinstance(y, str):
        y = float(y)

    ax.text(x, y, label, color=color, fontsize=18, horizontalalignment='center', verticalalignment='center')
