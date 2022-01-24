_gradebook_short_opts()
{
	local cur prev generic_opts calculate_opts new_opts names_opts
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	generic_opts="-h -v"
	calculate_opts="-h -s -q"
	new_opts="-h -t -n -d"
	names_opts="-h -l"

	if [[ ( "${prev}" == calc ) || ( "${prev}" == calculate ) ]]; then
		COMPREPLY=( $( compgen -W "${calculate_opts}" -- ${cur} ) )
	elif [[ "${prev}" == calculate ]]; then
		COMPREPLY=( $( compgen -W "${calculate_opts}" -- ${cur} ) )
	elif [[ "${prev}" == names ]]; then
		COMPREPLY=( $( compgen -W "${names_opts}" -- ${cur} ) )
	elif [[ "${prev}" == new ]]; then
		COMPREPLY=( $( compgen -W "${new_opts}" -- ${cur} ) )
	else
		COMPREPLY=( $( compgen -W "${generic_opts}" -- ${cur} ) )
	fi
}

_gradebook_long_opts()
{
	local cur prev generic_opts calculate_opts new_opts names_opts
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	pre_prev="${COMP_WORDS[COMP_CWORD-2]}"
	generic_opts="--help --version"
	calculate_opts="--help --semester --quarter"
	new_opts="--helt --type --name --date"
	names_opts="--help -last-first"

	if [[ ( "${prev}" == calc ) || ( "${prev}" == calculate ) ]]; then
		COMPREPLY=( $( compgen -W "${calculate_opts}" -- ${cur} ) )
	elif [[ "${prev}" == calculate ]]; then
		COMPREPLY=( $( compgen -W "${calculate_opts}" -- ${cur} ) )
	elif [[ "${prev}" == names ]]; then
		COMPREPLY=( $( compgen -W "${names_opts}" -- ${cur} ) )
	elif [[ "${prev}" == new ]]; then
		COMPREPLY=( $( compgen -W "${new_opts}" -- ${cur} ) )
	else
		COMPREPLY=( $( compgen -W "${generic_opts}" -- ${cur} ) )
	fi
}

_gradebook_commands()
{
	local cur prev commands
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	commands="calc calculate names new"

	COMPREPLY=( $( compgen -W "${commands}" -- ${cur} ) )
}

_gradebook_main()
{
	local cur prev pre_prev
	COMPREPLY=()
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"

	if [[ "${cur}" == --* ]]; then
		_gradebook_long_opts
	elif [[ "${cur}" == -* ]]; then
		_gradebook_short_opts
	elif [[ "${prev}" == gradebook ]]; then
		_gradebook_commands
	fi
}

complete -F _gradebook_main gradebook

# vim: set ts=4 sw=4 tw=75 filetype=sh:
