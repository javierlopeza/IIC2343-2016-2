import java.io.*;
import java.nio.file.*;
import javax.script.ScriptEngineManager;
import javax.script.ScriptEngine;
import java.math.*;

public class tarea2 {
	
    public static void main(String[] args){  

	    ScriptEngineManager mgr = new ScriptEngineManager();
	    ScriptEngine engine = mgr.getEngineByName("JavaScript");

    	try {
	    	FileReader fileReader = new FileReader(new File( args[0] ));
	
	    	BufferedReader br = new BufferedReader(fileReader);
	
	    	String line = null;
	    	// if no more lines the readLine() returns null
	    	 
    		while ((line = br.readLine()) != null) {
       	     	// reading lines until the end of the file

	    		String numRX = "^[-]?[0-9]+[/][0-9]+$|^[-]?[0-9]*[.][0-9]*$|^[-]?[0-9]+$";
	    		Boolean isNumeric = line.matches(numRX);

	    		if (isNumeric) {
	    			String fracRX = "^[-]?[0-9]+[/][0-9]+$";
	    			Boolean isFraction = line.matches(fracRX);
	    			String pointRX = "^[-]?[0-9]*[.][0-9]*$";
	    			Boolean isPointDecimal = line.matches(pointRX);

	    			if (isFraction) {

	    				//System.out.print("isFraction => ");

						String[] partsFrac = line.split("/");
						Long numerador = Long.parseLong( partsFrac[0] );
						Long denominador = Long.parseLong( partsFrac[1] );

						if (numerador != 0 && denominador == 0) {
						    if (line.startsWith("-")){
        						System.out.println(line + " => Float (-Infinity)");
        					}
        					else {
        						System.out.println(line + " => Float (Infinity)");
        					}
						}
						else if (numerador == 0 && denominador == 0) {
							System.out.println(line + " => Float (NaN)");
						}
						else if (numerador == 0 && denominador != 0) {
							System.out.println(line + " => Byte (0)");
						}
						else {
							//System.out.print("Numerador: " + numerador + "  Denominador: " + denominador);

							Boolean esEntero = ((numerador%denominador) == 0);

		    				if (esEntero) {
		    					//System.out.print("esEntero => ");

		    					String eval_line = (engine.eval(line)).toString();
		    					try {
						        	Byte b = Byte.valueOf( eval_line );
						        	System.out.println(line + " => Byte (" + b + ")");
						        }
						        catch( Exception e1 ) {
						            try {
						            	Short s = Short.parseShort( eval_line );
						            	System.out.println(line + " => Short (" + s + ")");
						            }
						            catch( Exception e2 ) {
						                try {
						                	Integer i = Integer.parseInt( eval_line );
						                	System.out.println(line + " => Int (" + i + ")");
						                }
						                catch( Exception e3 ) {
						                	try {
						                		Long l = Long.parseLong( eval_line );
						                		System.out.println(line + " => Long (" + l + ")");
						                	}
						                	catch( Exception e4 ){
						                		try {
						                			Float f = Float.parseFloat( eval_line );
						            				Boolean esInfinito = Float.isInfinite(f);
						            				if (esInfinito) {
						            					if (line.startsWith("-")){
						            						System.out.println(line + " => Float (-Infinity)");
						            					}
						            					else {
						            						System.out.println(line + " => Float (Infinity)");
						            					}
						            				}
						            				else {
						            					BigDecimal f_full = new BigDecimal(f);
		                								System.out.println(line + " => Float (" + f_full + ")");	
						            				}
						                		}
						                		catch( Exception e5){
						                			if( line.length() == 1){
						                				char c = line.charAt(0);
						                				System.out.println(line + " => Char");
						                			}
						                			else{
						                				System.out.println(line + " => String");
						                			}
						                		}
						                	}
						                }
						            } 
						        }
		    				}
		    				else {
		    					//System.out.print("NoEntero => ");
		    					String eval_line = engine.eval(line).toString();
		                		try {
		                			Float f = Float.parseFloat( eval_line );
		                			BigDecimal f_full = new BigDecimal(f);
		                			System.out.println(line + " => Float (" + f_full + ")");
		                		}
		                		catch( Exception e5){
		                			if( line.length() == 1){
		                				char c = line.charAt(0);
		                				System.out.println(line + " => Char");
		                			}
		                			else{
		                				System.out.println(line + " => String");
		                			}
		                		}
		    				}
						}

						
	    			}
	    			else if (isPointDecimal) {
	    				//System.out.print("hasPoint => ");

			    		String ceroRX = "^[-]?[0-9]*[.][0]*$";
			    		Boolean tieneParteDecimalCero = line.matches(ceroRX);
			    		if (tieneParteDecimalCero) {
			    			//System.out.print("TieneParteDecimalCero => ");

			    			String old_line = line;
			    			line = line.substring(0, line.indexOf( '.' ));
				    		try {
					        	Byte b = Byte.valueOf( line );
					        	System.out.println(old_line + " => Byte (" + b + ")");
					        }
					        catch( Exception e1 ) {
					            try {
					            	Short s = Short.parseShort( line );
					            	System.out.println(old_line + " => Short (" + s + ")");
					            }
					            catch( Exception e2 ) {
					                try {
					                	Integer i = Integer.parseInt( line );
					                	System.out.println(old_line + " => Int (" + i + ")");
					                }
					                catch( Exception e3 ) {
					                	try {
					                		Long l = Long.parseLong( line );
					                		System.out.println(old_line + " => Long (" + l + ")");
					                	}
					                	catch( Exception e4 ){
					                		try {
					                			Float f = Float.parseFloat( line );
					                			BigDecimal f_full = new BigDecimal(f);
	                							System.out.println(line + " => Float (" + f_full + ")");			                		
					                		}
					                		catch( Exception e5){
					                			if( old_line.length() == 1){
					                				char c = old_line.charAt(0);
					                				System.out.println(old_line + " => Char");
					                			}
					                			else{
					                				System.out.println(old_line + " => String");
					                			}
					                		}
					                	}
					                }
					            } 
					        }
				    	}
				    	else {
				    		//System.out.print("TieneParteDecimal => ");
				    		try {
					        	Byte b = Byte.valueOf( line );
					        	System.out.println(line + " => Byte (" + b + ")");
					        }
					        catch( Exception e1 ) {
					            try {
					            	Short s = Short.parseShort( line );
					            	System.out.println(line + " => Short (" + s + ")");
					            }
					            catch( Exception e2 ) {
					                try {
					                	Integer i = Integer.parseInt( line );
					                	System.out.println(line + " => Int (" + i + ")");
					                }
					                catch( Exception e3 ) {
					                	try {
					                		Long l = Long.parseLong( line );
					                		System.out.println(line + " => Long (" + l + ")");
					                	}
					                	catch( Exception e4 ){
					                		try {
					                			Float f = Float.parseFloat( line );
					            				Boolean esInfinito = Float.isInfinite(f);
					            				if (esInfinito) {
					            					if (line.startsWith("-")){
					            						System.out.println(line + " => Float (-Infinity)");
					            					}
					            					else {
					            						System.out.println(line + " => Float (Infinity)");
					            					}
					            				}
					            				else {
					            					BigDecimal f_full = new BigDecimal(f);
	                								System.out.println(line + " => Float (" + f_full + ")");	
					            				}
					                			
					                		}
					                		catch( Exception e5){
					                			if( line.length() == 1){
					                				char c = line.charAt(0);
					                				System.out.println(line + " => Char");
					                			}
					                			else{
					                				System.out.println(line + " => String");
					                			}
					                		}
					                	}
					                }
					            } 
					        }
				    	}
	    			}
	    			else{
	    				//System.out.print("EsEnteroOriginal => ");
	    				try {
				        	Byte b = Byte.valueOf( line );
				        	System.out.println(line + " => Byte");
				        }
				        catch( Exception e1 ) {
				            try {
				            	Short s = Short.parseShort( line );
				            	System.out.println(line + " => Short");
				            }
				            catch( Exception e2 ) {
				                try {
				                	Integer i = Integer.parseInt( line );
				                	System.out.println(line + " => Int");
				                }
				                catch( Exception e3 ) {
				                	try {
				                		Long l = Long.parseLong( line );
				                		System.out.println(line + " => Long");
				                	}
				                	catch( Exception e4 ){
				                		try {
				                			Float f = Float.parseFloat( line );
				                			BigDecimal f_full = new BigDecimal(f);
	                						System.out.println(line + " => Float (" + f_full + ")");			                		
				                		}
				                		catch( Exception e5){
				                			if( line.length() == 1){
				                				char c = line.charAt(0);
				                				System.out.println(line + " => Char");
				                			}
				                			else{
				                				System.out.println(line + " => String");
				                			}
				                		}
				                	}
				                }
				            } 
				        }
	    			}
	    		}
	    		else {
	    			//System.out.print("EsWord => ");
			        if( line.length() == 1){
        				char c = line.charAt(0);
        				System.out.println(line + " => Char");
        			}
        			else{
        				System.out.println(line + " => String");
        			}
	    		}

    		 }
    	 }
    	 catch( Exception eR ) {
		    System.out.println(eR);
    	 }
    }
}

/*
char c = args[0].charAt(0);
System.out.println("Es Char! " + c);

System.out.println("Es String! " + args[0]);

Byte b = Byte.valueOf( args[0] );
System.out.println("Es Byte! " + b);

Short s = Short.parseShort( args[0] );
System.out.println("Es Short! " + s);

Integer i = Integer.parseInt( args[0] );
System.out.println("Es Int! " + i);

Long l = Long.parseLong( args[0] );
System.out.println("Es Long! " + l);

Float f = Float.parseFloat( args[0] );
System.out.println("Es Float! " + f);
*/