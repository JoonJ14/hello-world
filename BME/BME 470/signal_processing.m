clear
load 'r01_edfm.mat'

x=(val(1,1:end))
fs=length(x)/10
time=(0:length(x)-1)/fs

subplot(4,1,1)
plot(time,x)
xlabel('Time(s)');
ylabel('Signal amplitude');

y=fft(x)
df=fs/length(y);
fv=df*(0:1:length(y)-1)

subplot(4,1,2)
plot(fv,abs(y));
xlabel('Frequency');
ylabel('Signal amplitude');
grid on 

lowcutoff=(40*10+1);
y1=y;
N=length(y)
y1(lowcutoff:N-lowcutoff)=0;

highcutoff=(5*10+1);
y1(1:highcutoff)=0
y1(N-highcutoff:N)=0

subplot(4,1,3)
plot(fv,abs(y1));
xlabel('Frequency');
ylabel('Signal amplitude');
grid on

yfilt=ifft(y1);

subplot(4,1,4)
plot(time, yfilt)
xlabel('Time(s)');
ylabel('Signal amplitude');