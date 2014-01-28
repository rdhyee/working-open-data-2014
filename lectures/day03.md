% Day 3:  Setting Up Cont'd: Environments and Contexts
% Raymond Yee 
% January 28, 2014 (<http://is.gd/wwod1403>)

# Goals Today

 * Administrative
    * Meet your tutor:  AJ Renold
	* Schedule office hours -- and correct location.
	* Let's keep using <http://bit.ly/wwod14classnotes> 
 * Basic orientation to Python environments
 * Checklist:  can everyone run a sample IPython notebook and upload
   to bCourses

 * My goal:  to make WwOD FUN, ENGAGING, and NOT OVERWHELMING

**I want people to ask questions and flag stuff that's confusing**

# Meet AJ Renold, the Course Tutor

AJ Renold is wonderful:  kind, smart, and responsive. Get to know him.

His role:

* maintain activity on canvas and to create useful examples for
 students who are struggling with elementary python, shell, and git.
* holding office hours
* helping RY with eventually grading assignments (or working on automation tools)

# Assumed Background Knowledge

* Certain skills that would be very useful for us to work on if we don't
already have. I will actually use them in course.

The skills include:

* elementary Python
* working with the Unix shell
* source control, specifically git and github

Material you'll find in <http://software-carpentry.org/v4/index.html> for
example.

* Please flag things that are unclear by posting questions to
  bCourses. 

* Work with AJ to get up to speed.

* Should many people struggle with certain skills/knowledge areas,
we'll consider providing more training and taking up some issues
during class.

# Office Hours

Thanks to everyone who took the 
[Doodle: Office Hour choices](http://doodle.com/38txkgm48qyr8z7w).
I'm going to leave my office hours at Tues, Thurs 3:30-4:30pm in **302
South Hall**.  We start today and run until the end of the semester --
unless I make an announcement canceling an office hour.

I'm willing to schedule other meetings and virtual
office hours as the need arises.  (For example, I'm a fan of Google
Hangout, and the campus has a new video-conferencing system we can try
out or the
[Web Conferences in Working with Open Data](https://bcourses.berkeley.edu/courses/1189091/conferences).  

[Faculty Office Hours | School of Information](http://www.ischool.berkeley.edu/people/faculty/officehours)

For info about AJ's office hours, see
[bCourses: AJ's Office Hours for Working With Open Data](https://bcourses.berkeley.edu/courses/1189091/discussion_topics/2915734).

# Assignments from Last Week

[Working with Open Data: Assignments](https://bcourses.berkeley.edu/courses/1189091/assignments)
-- about 38 people submitted assignments.

**When can I expect the remainder of class to submit assignments?**

For this round, I will accept late submissions.

Results of survey of student background:
[Survey about Technical Background: Statistics](https://bcourses.berkeley.edu/courses/1189091/quizzes/1528658/statistics)


# Abstractions in our work

Lots of things happen when we run a Python program or run a cell in
an IPython notebook.  Most we can take for granted, but sometimes we
need to understand some of the underlying complexity.

Much work goes into allowing us to work with **abstractions** but beware
[The Law of Leaky Abstractions](http://www.joelonsoftware.com/articles/LeakyAbstractions.html).

The core of this course is using **Python** to work with **data**
(particularly **open data**.)

# Many Things at Work in "Simple" Computation

But consider, for a moment, all the things associated with the
"simple" act of running a Python program or an IPython notebook:

* the actual version of Python we are using  (v 2.7.6 vs. v 3.3
  vs. v 2.6 -- what difference does it make?)
* operating system used
* using a Python shell, a command line, inside of IPython Notebook, etc?
* the computer hardware used to run the program
    *  CPUs
    *  storage
    *  memory
    * input/output:  network bandwidth
    * virtualization involved?
* the "network":  Internet, in particularly the WWW
* how we might interact with the execution environment:
    * using a terminal with command line interface
    * typing in a web browser
    * local vs remote execution

# The Culture of Software Development

* Why use Python?  What alternatives?  Use programming languages together?
* free/open source software vs proprietary software -- what are the
  tradeoffs?
* workflow for working alone and together
    * use of  source control: git, github
* software engineering practices
    * pair programming
    * test-driven development

# A few Questions about the Data

* who authored it?
* where to access it?
* web scraping vs APIs vs bulk data access
* "processed data" vs [Raw data](https://en.wikipedia.org/wiki/Raw_data)

# RY's philosophy for learning how to work with data

I have a philosophy to guide ourselves in this course

* philosophy of immersion:  often we jump in and then figure stuff out
  as we go.
* developing [toeholds](http://www.thefreedictionary.com/toeholds) of
  the mind
* working code is gold -- hang on to it...and leverage it and work
  hard to keep things working code working
* confusion is not surprising for anyone, novice and expert alike
* experts learn to deal with confusion.
* Hang in there -- your persistence will pay off: [Things I Wish Someone Had Told Me When I Was Learning How to Code Learning to Code](https://medium.com/learning-to-code/565fc9dcb329)
* coding is social practice: [reflecting on Introduction to Python for Librarians](http://andromedayelton.com/blog/2013/11/25/reflecting-on-introduction-to-python-for-librarians/)

# Learning to Program is a bit Like learning a natural language

* You got to practice to develop fluency
* We learn together
* We learn by making mistakes

# Key Concept for Today:  Execution Environment of Python

What is an execution environment? [Python Essential Reference, Fourth Edition> Execution Environment : Safari Books Online](http://my.safaribooksonline.com/book/programming/python/9780768687040/the-python-language/ch10)

Python:
([Core Language](http://docs.python.org/2/reference/index.html#reference-index) +
[Standard Library](http://docs.python.org/2/library/))
+ other installed packages

* versions matter: version of Python Python versions + versions of packages

* Python core language + any Python packages installed --> _often_
   run across different contexts (operating systems)

Typically, the quotidian question we have is:  **how to install a
given Python package**

# Major Alternatives to Package Installers

I would say that [pip](http://www.pip-installer.org/en/latest/) is a
central tool for installing packages -- especially because of the
great [PyPI](https://pypi.python.org/pypi) "repository of software for
the Python programming language."

But there are times, it's actually really hard to get certain packages
installed...and there's where I really appreciate Python distributions
along with their package installer.

For this course, we recommend Anaconda:  see
[IPython Installation Options · rdhyee/working-open-data-2014 Wiki](https://github.com/rdhyee/working-open-data-2014/wiki/IPython-Installation-Options).

(BTW, anyone can edit the course github wiki).

# Wakari vs Anaconda

I recommended Wakari to start because it's easy to set up:  create an
account on wakari.io and you can go...

Think about the trade offs betwen running on your laptop ([Anaconda](https://store.continuum.io/cshop/anaconda/)) vs running on a virtualized Python environment
running on the continuum.io servers (Wakari)

Wakari is good to have around but I think everyone will be happier  having IPython notebook running on their own laptops.

I encourage you to install the anaconda python distribution even if
already have another one running.

# Conda

[Conda — Continuum documentation](http://docs.continuum.io/conda/) is
a Anaconda-specific alternative to
[virtualenv](https://pypi.python.org/pypi/virtualenv)/[virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/).

Conda [to quote the Conda docs]:

* "primary interface for managing Anaconda installations."
* "It can query and search the Anaconda package index and current
 Anaconda installation"
* "create new Anaconda environments"
* "install and update packages into existing Anaconda environments"

[Examples — Continuum documentation](http://docs.continuum.io/conda/examples.html)

# How I use conda

* In my specific case, I'm running OS X 10.6.8.  When I downloaded and
installed anaconda, all my anaconda files end up in `~/anaconda`.

* A really nice [feature](https://store.continuum.io/cshop/anaconda/): "installs into a single directory and doesn't affect other Python installations on your system. Doesn't require root or local administrator privileges."

* On my Mac, the key to swapping between using Anaconda environments
  and my virtualenvs is through __manipulating the \$PATH environment
  variable__.  If I want to use anaconda, I need to get `~/anaconda/bin`
  to beginning of `$PATH` -- see
  [Anaconda FAQ — Continuum documentation](http://docs.continuum.io/anaconda/faq.html#install-maclinux)
  conda environments

* I have an alias defined in my `~/.profile` to make this easier to do
  on the fly:

		# have alias for using anaconda
		alias use_conda='export ANACONDA_HOME=$HOME/anaconda; export PATH=$ANACONDA_HOME/bin:$PATH;'

* My conda environments are found in `~/anaconda/envs`.  To get rid of
  an environment, just delete the corresponding subdirectory.

* Note:  wakari also uses Conda: [Custom Python Environments in Wakari](http://continuum.io/blog/wakari_custom_envs)

# Conda invocations I've found Useful

`conda info`: tells you things like what your default environment is.
`conda --help`:  to get help

[Packages included in Anaconda 1.8.0 — Continuum documentation](about:blank)

# creating a minimalist conda environment

Just Python 2.7.6 and `pip` (and some other basic packages deemed
important by conda):

To create minimal env and activate it:

    conda create --no-default-packages -n minimal python=2.7.6 pip

	source activate minimal

To list packages installed by conda:

	conda list

To leave this environment:

	source deactivate

[One issue that I've not worked out:  `source activate minimal` should actually remove `~/anaconda/bin` from my `\$PATH` so I don't end up accidentally using the base installation when I don't want to.]

# a maximalist environment

What I call `myenv` -- install everything in anaconda:

	conda create -n myenv anaconda

# a IPython-dev environment

	conda create -n ipython-dev ipython-notebook ipython-qtconsole pip
    matplotlib numpy pandas

I then install the master branch of IPython into this environment: [Quickstart — IPython 1.1.0: An Afternoon Hack documentation](http://ipython.org/ipython-doc/stable/install/install.html)

# Using the Course Github site:

	git clone https://github.com/rdhyee/working-open-data-2014.git

If you don't know how to use git/github, it's time to learn.  

#  Conda environments to Possibly Use

It is possible to use anaconda w/o defining any environments, but I
recommend using them to control for dependencies.

# installing census package

	pip install -U census

# Wakari custom environments

I'll show you in class how to use conda in Wakari -- think about
what's going on in the Linux environments running on the Wakari machines

[Custom Python Environments in Wakari](http://continuum.io/blog/wakari_custom_envs)
  
# Assignments / Homework

[Day_02_A_US_Census_API.ipynb](https://bcourses.berkeley.edu/courses/1189091/assignments/4496113):
Fill in the notebook
[working-open-data-2014/notebooks/Day_02_A_US_Census_API.ipynb at master · rdhyee/working-open-data-2014](https://github.com/rdhyee/working-open-data-2014/blob/master/notebooks/Day_02_A_US_Census_API.ipynb).
Due **Friday, Jan 31, 2014 at 11:59pm PST**

