x=signal(:,1)

x=0
count=0
for i=1:length(y)
    if y(i)>=450 && y(i+1)<450
        count=count+1
    end
end

      
    