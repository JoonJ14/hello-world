function varargout = test3_final(varargin)
% TEST3_FINAL MATLAB code for test3_final.fig
%      TEST3_FINAL, by itself, creates a new TEST3_FINAL or raises the existing
%      singleton*.
%
%      H = TEST3_FINAL returns the handle to a new TEST3_FINAL or the handle to
%      the existing singleton*.
%
%      TEST3_FINAL('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in TEST3_FINAL.M with the given input arguments.
%
%      TEST3_FINAL('Property','Value',...) creates a new TEST3_FINAL or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before test3_final_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to test3_final_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help test3_final

% Last Modified by GUIDE v2.5 16-Nov-2018 22:22:40

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @test3_final_OpeningFcn, ...
                   'gui_OutputFcn',  @test3_final_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before test3_final is made visible.
function test3_final_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to test3_final (see VARARGIN)

% Choose default command line output for test3_final
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes test3_final wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = test3_final_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
file=uigetfile()
load(file)
global time
global y
global fv

x=(val(1,1:end));
fs=length(x)/10;
time=(0:length(x)-1)/fs;

axes(handles.axes1)
plot(time,x)
xlabel('Time(s)');
ylabel('Signal amplitude');

y=fft(x);
df=fs/length(y);
fv=df*(0:1:length(y)-1);

axes(handles.axes2)
plot(fv,abs(y));
xlabel('Frequency');
ylabel('Signal amplitude');
grid on 


function edit1_Callback(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit1 as text
%        str2double(get(hObject,'String')) returns contents of edit1 as a double
global lowfilt
lowfilt=str2double(get(hObject,'String'))


% --- Executes during object creation, after setting all properties.
function edit1_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function edit2_Callback(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit2 as text
%        str2double(get(hObject,'String')) returns contents of edit2 as a double
global highfilt
highfilt=str2double(get(hObject,'String'))



% --- Executes during object creation, after setting all properties.
function edit2_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in pushbutton2.
function pushbutton2_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton2 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global fv
global y
global time
global lowfilt
global highfilt

y1=y
lowcutoff=(lowfilt*10+1);
N=length(y)
y1(lowcutoff:N-lowcutoff)=0;

highcutoff=(highfilt*10+1)
N=length(y)
y1(1:highcutoff)=0
y1(N-highcutoff:N)=0

axes(handles.axes3)
plot(fv,abs(y1));
xlabel('Frequency');
ylabel('Signal amplitude');
grid on

yfilt=ifft(y1);

axes(handles.axes4)
plot(time, yfilt)
xlabel('Time(s)');
ylabel('Signal amplitude');


function edit3_Callback(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of edit3 as text
%        str2double(get(hObject,'String')) returns contents of edit3 as a double



% --- Executes during object creation, after setting all properties.
function edit3_CreateFcn(hObject, eventdata, handles)
% hObject    handle to edit3 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end
