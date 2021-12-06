program day04
    implicit none

    integer, allocatable, dimension(:) :: draws, test_draws
    integer, allocatable, dimension(:,:) :: boards, test_boards

    integer :: solution_1, solution_2

    call load_data("test_input.txt", test_draws, test_boards)
    call load_data("input.txt", draws, boards)

    solution_1 = solve_part1(test_draws, test_boards)
    call assert_equal(solution_1, 4512)

    solution_1 = solve_part1(draws, boards)
    call assert_equal(solution_1, 44736)

    print *, "The solution to part 1 is ", solution_1
    print *

    solution_2 = solve_part2(test_draws, test_boards)
    call assert_equal(solution_2, 1924)

    solution_2 = solve_part2(draws, boards)
    call assert_equal(solution_2, 1827)

    print *, "The solution to part 2 is ", solution_2

contains

    subroutine load_data(filename, draws, boards)
        character(*), intent(in) :: filename
        integer, intent(out), allocatable, dimension(:) :: draws
        integer, intent(out), allocatable, dimension(:,:) :: boards

        character(len=1000) :: draw_buffer, buffer

        integer :: i, num_lines, num_draws

        open(2, file=filename, status="old")

        read (2,"(A)") draw_buffer

        num_draws = 1
        do i = 1,len(trim(draw_buffer))
            if (draw_buffer(i:i) == ",") then
                num_draws = num_draws + 1
            end if
        end do

        num_lines = 0
        do i = 1,1000
            read (2,*,end=100) buffer
            num_lines = num_lines + 1
        end do

    100 rewind(2)

        allocate(draws(num_draws))
        allocate(boards(num_lines, 5))

        read (2,*) draws
        read (2,*) (boards(i,:), i=1,num_lines)

        close(2)
    end subroutine load_data


    function is_in_array(val, arr) result (is_in)
        integer, intent(in) :: val
        integer, intent(in), dimension(:) :: arr

        logical :: is_in
        integer :: i

        is_in = .false.
        do i = 1,size(arr)
            if (val == arr(i)) then
                is_in = .true.
                return
            end if
        end do
    end function is_in_array


    function is_winning_board(draws, board) result (is_winning)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(5,5) :: board

        integer :: num_draws
        logical :: is_winning
        integer :: row, col

        num_draws = size(draws)

        do row = 1,5
            do col = 1,5
                is_winning = .true.
                if (.not. is_in_array(board(row,col), draws(1:num_draws))) then
                    is_winning = .false.
                    goto 100
                end if
            end do
            if (is_winning) then
                return
            end if
    100     continue
        end do

        do col = 1,5
            do row = 1,5
                is_winning = .true.
                if (.not. is_in_array(board(row,col), draws(1:num_draws))) then
                    is_winning = .false.
                    goto 200
                end if
            end do
            if (is_winning) then
                return
            end if
    200     continue
        end do

        is_winning = .false.

    end function is_winning_board


    function sum_remaining(draws, board) result (result)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(5,5) :: board

        integer :: num_draws
        integer :: i, j
        integer :: result

        num_draws = size(draws)

        result = 0
        do i=1,5
            do j=1,5
                if (.not. is_in_array(board(i,j), draws(1:num_draws))) then
                    result = result + board(i,j)
                end if
            end do
        end do
    end function sum_remaining


    function solve_part1(draws, boards) result (x)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(:,:) :: boards

        integer, dimension(5,5) :: board
        integer :: x

        integer :: num_draws, num_boards
        integer :: i, j, k

        num_draws = size(draws, 1)
        num_boards = size(boards, 1) / 5

        do i = 1,num_draws
            do j = 1,num_boards
                board = boards(5*(j-1)+1:5*(j-1)+5, :)
                if (is_winning_board(draws(1:i), board)) then
                    x = sum_remaining(draws(1:i), board) * draws(i)
                    return
                end if
            end do
        end do
    end function solve_part1


    function solve_part2(draws, boards) result (result)
        integer, intent(in), dimension(:) :: draws
        integer, intent(in), dimension(:,:) :: boards

        integer, dimension(5,5) :: board
        integer, allocatable, dimension(:) :: is_winning
        integer :: result
        integer :: num_draws, num_boards
        integer :: i, j

        num_draws = size(draws, 1)
        num_boards = size(boards, 1) / 5

        allocate(is_winning(num_boards))

        is_winning = 0
        do i = 1,num_draws
            do j = 1,num_boards
                board = boards(5*(j-1)+1:5*(j-1)+5, :)
                if (is_winning_board(draws(1:i), board)) then
                    if (sum(is_winning) == num_boards - 1 .and. .not. is_winning(j) == 1) then
                        result = sum_remaining(draws(1:i), board) * draws(i)
                        return
                    end if
                    is_winning(j) = 1
                end if
            end do
        end do
    end function solve_part2


    subroutine assert_equal(actual, expected)
        integer :: actual, expected

        if (actual .ne. expected) then
            print *, "ASSERTION FAILED, ", actual, "!=", expected
            call exit(1)
        end if
    end subroutine assert_equal

end program day04
