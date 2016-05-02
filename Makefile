target:
	javac DBO.java
	javac FeiguHandler.java -cp .:../lib/* 
clean:
	rm *.class
