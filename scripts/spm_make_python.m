function spm_make_python(outdir)
%
% outdir - Path to working/output directory.
%          If this path contains `external/spm` and `external/mpython`
%          folders, they will be used. Otherwise, they will be pulled
%          from github.
%
% Compile SPM as a Python-enabled CTF file using the MATLAB Compiler
%   https://www.mathworks.com/products/compiler.html
%
% When deployed, compiled applications will require the MATLAB Runtime:
%   https://www.mathworks.com/products/compiler/matlab-runtime.html
%__________________________________________________________________________

% Adapted from spm_make_standalone
% Johan Medrano, Guillaume Flandin
% Copyright (C) 2010-2025 Wellcome Centre for Human Neuroimaging

if nargin < 1, [outdir, ~, ~] = fileparts(mfilename('fullpath')); end

cd(outdir);

% -------------------------------------------------------------------------
% External directory that contains spm and mpython
% -------------------------------------------------------------------------
if ~exist('external', 'dir'), mkdir('external'); end
cd('external')
if ~exist('spm', 'dir')
    system('git clone --depth=1 https://github.com/spm/spm.git');
end
if ~exist('mpython', 'dir')
    system('git clone --depth=1 https://github.com/MPython-Package-Factory/mpython.git');
end
cd('..')

% -------------------------------------------------------------------------
% Directory that contains a "cleaned up" version of spm
% -------------------------------------------------------------------------
if exist('cleaned', 'dir')
    rmdir('cleaned', 's');
end
mkdir('cleaned')

spmpath = fullfile(outdir, 'cleaned', 'spm');
copyfile(fullfile('external', 'spm'), spmpath, 'f');

restoredefaultpath
addpath(fullfile('external', 'mpython'), spmpath);
spm('defaults', 'eeg');
spm_jobman('initcfg')

% Create Contents.txt file used by spm('version')
copyfile(fullfile(spm('Dir'),'Contents.m'),...
         fullfile(spm('Dir'),'Contents.txt'));

ignored = {...
    '.git', ...
    '.github', ...
    'external/fieldtrip/compat/*', ...
    'external/fieldtrip/.git', ...
    'external/fieldtrip/.github',...
    'toolbox/DEM/VOX.mat',...
    'toolbox/DEM/DEM_lorenz_suprise.mat',...
    'toolbox/DEM/DEM_IMG.mat',...
    'toolbox/DEM/ADEM_saccades.mat',...
};
for d = ignored
    try
        rmdir(fullfile(spmpath, d{1}), 's');
    end
    try
        delete(fullfile(spmpath, d{1}));
    end
end

% -------------------------------------------------------------------------
% Static listing of SPM toolboxes
% -------------------------------------------------------------------------
fid = fopen(fullfile(spm('Dir'),'config','spm_cfg_static_tools.m'),'wt');
fprintf(fid,'function values = spm_cfg_static_tools\n');
fprintf(fid,...
    '%% Static listing of all batch configuration files in the SPM toolbox folder\n');
%-Get the list of toolbox directories
tbxdir = fullfile(spm('Dir'),'toolbox');
d = [tbxdir; cellstr(spm_select('FPList',tbxdir,'dir'))];
ft = {};
%-Look for '*_cfg_*.m' files in these directories
for i=1:numel(d)
    fi = spm_select('List',d{i},'.*_cfg_.*\.m$');
    if ~isempty(fi)
        ft = [ft(:); cellstr(fi)];
    end
end
%-Create code to insert toolbox config
if isempty(ft)
    ftstr = '';
else
    ft = spm_file(ft,'basename');
    ftstr = sprintf('%s ', ft{:});
end
fprintf(fid,'values = {%s};\n', ftstr);
fclose(fid);

% -------------------------------------------------------------------------
% Static listing of batch application initialisation files
% -------------------------------------------------------------------------
cfg_util('dumpcfg');

% -------------------------------------------------------------------------
% Compile
% -------------------------------------------------------------------------
toolboxes = {'parfor', 'stats', 'images', 'signal'};
mpython_compile(spmpath, outdir, 'spm', toolboxes)

disp('Done!');
