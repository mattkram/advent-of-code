module procedures
    implicit none

contains
    subroutine load_data(filename, draws, boards)
        character(*), intent(in) :: filename
        integer, intent(out), dimension(:) :: draws
        integer, intent(out), dimension(:,:) :: boards

        integer i

!        print *, filename
        open(2, file=filename, status="old")

        read (2,*) draws
!        print *, draws

!        print *, "Puzzle input:"
        do i = 1,15
            read (2,*) boards(i,:)
!            print *, boards(i,:)
!            if (mod(i, 5) == 0) then
!                print *, ""
!            end if
        end do

        close(2)
    end subroutine load_data


    function is_in_array(val, arr, num) result (is_in)
        integer, intent(in) :: val, num
        integer, intent(in), dimension(:) :: arr

        logical :: is_in

        integer :: i


        is_in = .false.

        do i = 1,num
            if (val == arr(i)) then
                is_in = .true.
                return
            end if
        end do

    end function is_in_array


    subroutine print_board(board)

    integer, intent(in), dimension(5,5) :: board

    integer :: i

    do i=1,5
        print *, board(i,:)
    end do
    print *, ""

    end subroutine print_board


    function is_winning_board(draws, board, num_draws) result (is_winning)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(5,5) :: board
        integer, intent(in) :: num_draws

        logical :: is_winning

        integer :: i, ii, row, col, rowi, coli

        is_winning = .false.

!        print *, "Board"
!        call print_board(board)

        do row = 1,5
            do col = 1,5
                is_winning = .true.
                if (.not. is_in_array(board(row,col), draws(1:num_draws), num_draws)) then
                    is_winning = .false.
                    goto 100
                end if
            end do
            if (is_winning) then
!                print *, "Winning board"
!                call print_board(board)
                return
            end if
            100 continue
        end do

        do coli = 1,5
            do rowi = 1,5
                is_winning = .true.
                if (.not. is_in_array(board(rowi,coli), draws(1:num_draws), num_draws)) then
                    is_winning = .false.
                    goto 200
                end if
            end do
            if (is_winning) then
!                print *, "Winning board"
!                call print_board(board)
                return
            end if
            200 continue
        end do

        is_winning = .false.

    end function is_winning_board


    function sum_remaining(draws, board, num_draws) result (rslt)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(5,5) :: board
        integer, intent(in) :: num_draws

        integer :: i, j
        integer :: rslt
        rslt = 0

        do i=1,5
            do j=1,5
                if (.not. is_in_array(board(i,j), draws(1:num_draws), num_draws)) then
                    rslt = rslt + board(i,j)
                end if
            end do
        end do

    end function sum_remaining


    function solve_part1(draws, boards) result (x)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(:,:) :: boards

        integer, dimension(5,5) :: board
        integer :: x

        integer :: i, j, k

        do i = 1,27
            do j = 1,3
                board = boards(5*(j-1)+1:5*(j-1)+5, :)
!                print *, "Board ", j
!                call print_board(board)

                if (is_winning_board(draws, board, i)) then
                    x = sum_remaining(draws, board, i) * draws(i)
                    return
                end if
            end do
        end do

        x = -1

    end function solve_part1


    function solve_part2(draws, boards) result (x)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(:,:) :: boards

        integer, dimension(5,5) :: board
        integer :: x

        integer :: i, j, k, m

        integer, dimension(3) :: is_winning
        do m=1,3
            is_winning(m) = 0
        end do

        do i = 1,27
            do j = 1,3
                board = boards(5*(j-1)+1:5*(j-1)+5, :)
                if (is_winning_board(draws, board, i)) then
                    if (sum(is_winning) == 2 .and. .not. is_winning(j) == 1) then
                        x = sum_remaining(draws, board, i) * draws(i)
                        return
                    end if
                    is_winning(j) = 1
                end if
            end do
        end do

        x = -1

    end function solve_part2


    subroutine assert_equal(actual, expected)
        integer :: actual, expected

        if (actual .ne. expected) then
            print *, "ASSERTION FAILED, ", actual, "!=", expected
            call exit(1)
        end if
    end subroutine assert_equal

end module procedures


program day04
    use procedures

    implicit none

    integer, dimension(27) :: draws
    integer, dimension(15,5) :: boards

    integer :: solution_1, solution_2

    call load_data("test_input.txt", draws, boards)

    solution_1 = solve_part1(draws, boards)
    print *, "The solution to part 1 is ", solution_1
    print *, "The expected solution  is         4512"
    print *
    call assert_equal(solution_1, 4512)

    solution_2 = solve_part2(draws, boards)
    print *, "The solution to part 2 is ", solution_2
    print *, "The expected solution  is         1924"
    call assert_equal(solution_2, 1924)

end program day04
