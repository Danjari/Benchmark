%%%%
%%%% This style file was created by Prof. Azza Abouzied
%%%% It modifies the ACM 2020 conference template.
%%%% It was last updated in Jan 27, 2020
%%%%
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{capstone}
\RequirePackage{graphicx}
\RequirePackage{epstopdf}
\RequirePackage{epsfig}
\RequirePackage{ifthen}
\RequirePackage{xspace}
\DeclareGraphicsExtensions{.eps}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{acmartmod}}
\ProcessOptions
\LoadClass[format=sigconf,10pt]{stylefiles/acmartmod} % we always use letter paper

\def\advisors#1{\def\@advisors{#1}}
\def\capstoneyear#1{\def\@capstoneyear{#1}}
%\newcommand{\advisors}[1]{\renewcommand{\@advisors}{#1}

\def\capstonedocument#1{\def\@capstonedocument{#1}}
\def\capstonesemester#1{\def\@capstonesemester{#1}}

\setcopyright{nyuad}
\copyrightyear{\@capstoneyear}
\acmYear{\@capstoneyear}
\acmDOI{}

%% These commands are for a PROCEEDINGS abstract or paper.
\acmConference[Capstone \@capstonedocument\xspace]{Capstone \@capstonedocument: NYUAD Capstone \@capstonedocument\xspace Reports}{\@capstonesemester\xspace \@capstoneyear}{Abu Dhabi, UAE}
\acmBooktitle{NYUAD Capstone \@capstonedocument\xspace Reports, \@capstonesemester\xspace \@capstoneyear, Abu Dhabi, UAE}
\acmPrice{}
\acmISBN{}

% \newsavebox{\departmenthead}
% \newsavebox{\departmentfoot}
% \newsavebox{\emptyfoot}

% \sbox{\departmenthead}{
%     \begin{tabular*}{\textwidth}
%                     {@{}l@{\extracolsep{0.0in}}|@{\extracolsep{0.125in}}l@{}}
%     \parbox{3.625in}{\raggedright
%         \ifthenelse{\boolean{logofound}}
%           {\includegraphics[width=2.0in]{images/nyuad-logo.png}}
%           {\parbox[t][1.0in][t]{2.0in}{\hfill} 
%             \ClassWarning{nyuadletter}{images/nyuad-logo.png COULD NOT BE FOUND!}}
%     } & 
%     \parbox[t][1.25in]{3in}{{\small Dr. Azza Abouzied \\ Assistant Professor of Computer Science \\ Computational Research Building, CRB-177\\
%     New York University Abu Dhabi \\ Saadiyat Island, Abu Dhabi, UAE \\
%     T: +971-2-628-5170 \\ E: \url{azza@nyu.edu}}}
%     % \parbox[t][1.0in]{2.125in}{{\sf Computer Science}\\
%     %                           {\sf https://nyuad.nyu.edu/}}\\
%     \\
%     & \\
%     %\hline
%     \end{tabular*}
% }

% \savebox{\departmentfoot}[\textwidth][c]{\footnotesize
%     New York University Abu Dhabi, 
%     ~P.O.Box 129188,
%     ~Saadiyat Island, Abu Dhabi
%     ~UAE
% }

% \savebox{\emptyfoot}[\textwidth][c]{
%     \hspace*{\textwidth}
% }

% % header and footer should be placed only on the first page
% \renewcommand{\ps@firstpage}{
%     \setlength{\headheight}{1.375in}
%     \setlength{\headsep}{1.0in}
%     \renewcommand{\@oddhead}{\usebox{\departmenthead}}
%     \renewcommand{\@oddfoot}{\usebox{\departmentfoot}}
%     \renewcommand{\@evenhead}{}
%     \renewcommand{\@evenfoot}{\usebox{\departmentfoot}}
% }

% \renewcommand{\ps@empty}{
%     \setlength{\headheight}{1.375in}
%     \setlength{\headsep}{0.5in}
%     \renewcommand{\@oddhead}{}
%     \renewcommand{\@oddfoot}{\usebox{\departmentfoot}}
%     \renewcommand{\@evenhead}{}
%     \renewcommand{\@evenfoot}{\usebox{\departmentfoot}}
% }

% \providecommand{\@evenhead}{}
% \providecommand{\@oddhead}{}
% \providecommand{\@evenfoot}{}
% \providecommand{\@oddfoot}{}

% \pagestyle{empty}

% % we add the subject command to the opening
% \renewcommand{\opening}[1]{\thispagestyle{firstpage}%
%     \ifx\@empty\fromaddress
%         {\raggedright\@date\par}%
%     \else  % home address
%         {\raggedright
%             %\begin{tabular}{l@{}}\ignorespaces
%             \fromaddress \\ *[1\parskip]%
%             \@date 
%             %\end{tabular}
%             \par
%         }%
%      \fi
%      \vspace{1\parskip}%
%      {\raggedright \toname \\ \toaddress \par}%
%      \vspace{1\parskip}%
%      \ifthenelse{\equal{\@subject}{}}{}{{\bf \@subject}\par}
%      \vspace{1\parskip}%
%      #1\par\nobreak
% }

% % we push closing to the right
% \renewcommand{\closing}[1]{\par\nobreak\vspace{\parskip}%
%     \stopbreaks
%     \noindent
%     \hspace*{0.6\textwidth}\parbox{0.4\textwidth}{\raggedright
%     \ignorespaces #1\\[1\medskipamount]%
%     %\ifx\@empty\fromsig
%         \quad\quad\includegraphics[height=0.4in]{images/signature.png}\\
%         %\fromname
%         \fromsig
%     %\else \fromsig 
%     %\fi\strut
        
%     }%
%     \par
% }