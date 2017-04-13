name "14632128 Tarea 4"

org 100h

; ----- CODE -----
whilelensize:
	MOV DI,0				; DI = r = 0
	whileDIsize:
		MOV CL,1				; CL = isZeroRow = True

		MOV AL,[size]			; BX = pointer = size * r  +  dir[graph]
		MUL DI 	 				
		LEA BX,graph
		ADD BX,AX

		MOV DH,0				; DH = i = 0
		whileDHsize1:
			CMP [BX],1
			JNE continuewhileDHsize1

				MOV CL,0			; CL = isZeroRow = False
				MOV DH,[size]		; DH = i = size

			continuewhileDHsize1:
				ADD BX,1			; BX += 1	
				ADD DH,1			; DH += 1
				CMP DH,[size]
				JL whileDHsize1

		CMP CL,1					; if isZeroRow == True:
		JNE isNotZeroRow

		isZeroRow:
			MOV AX,DI
			ADD AL,1				; AL = DI + 1
			MOV CL,0				; CL = alreadyIn = False
			LEA BX,ordering_aux 	; BX = dir[ordering_aux] 

			MOV CH,0
			whileCHsize: 			; while CH < size:
				CMP [BX],AL    		; if ordering_aux[BX] == AL:
				JE endwhileCHsize1

				CMP [BX],0
				JE endwhileCHsize2

				continuewhileCHsize:
					ADD BX,1			; BX += 1
					ADD CH,1			; CH += 1
					CMP CH,[size]
					JL whileCHsize

				endwhileCHsize1:
					MOV CL,1			; alreadyIn = True

				endwhileCHsize2:

			CMP CL,1			
			JE isNotZeroRow	; if alreadyIn == True:

			; if alreadyIn == False:
			LEA BX,graph 				; BX = dir[graph]
			ADD BX,DI 					; BX += DI
			MOV DH,0					; DH = 0
			MOV AL,[size]				; AL = size
			whileDHsize2:				; while DH < size:
				MOV [BX],0					; adjmatrix[BX] = 0
				ADD BX,AX 					; BX += AL
				ADD DH,1					; DH += 1
				CMP DH,[size]
				JL whileDHsize2

			LEA BX,ordering_aux 		; BX = dir[ordering_aux]
			MOV AL,[len_graph_sorted] 	; AL = len_graph_sorted
			ADD BX,AX 					; BX += AL
			MOV CX,DI 					; 
			ADD CL,1					; CL = DI + 1
			MOV [BX],CL 				; ordering_aux[BX] = DI+1
			ADD [len_graph_sorted],1	; len_graph_sorted += 1

			ADD AL,1
			CMP AL,[size]
			JE reverse

		isNotZeroRow:
			ADD DI,1
			MOV AX,DI
			CMP AL,[size]
			JL whileDIsize

		MOV DH,[len_graph_sorted]
		CMP DH,[size]
		JL whilelensize

; --- reverse result ---

reverse:
MOV DX,0
MOV CX,0
MOV DL,[size]
SUB DL,1

whilereverse:
	LEA BX,ordering_aux
	ADD BX,DX
	MOV AL,[BX]

	LEA BX,ordering
	MOV CL,[size]
	SUB CL,1
	SUB CL,DL
	ADD BX,CX

	MOV [BX],AL

	SUB DL,1

	CMP DL,-1
	JNE whilereverse


; ----- ret -----

; wait for any key press:
mov ah, 0
int 16h

ret

; ----- DATA -----  10 nodos
size 				db 10
graph 				db 0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0
ordering 			db 0,0,0,0,0,0,0,0,0,0
; variables auxiliares :
ordering_aux 		db 0,0,0,0,0,0,0,0,0,0
len_graph_sorted	db 0