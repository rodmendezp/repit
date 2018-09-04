const filters = {
    // From here all filters are intended to return true/false and not 'filtered' data
    isEmpty(s) {
        return typeof s === 'string' && s.length === 0;
    },
    notEmpty(s) {
        return !filters.isEmpty(s);
    },
    isEmail(s) {
        /* eslint no-useless-escape: 0 */
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(s).toLowerCase());
    },
    notEmail(s) {
        return !filters.isEmail(s);
    },
    maxLength(s, params = { max: 0 }) {
        return s.length <= params.max;
    },
    minLength(s, params = { min: 0 }) {
        return s.length >= params.min;
    },
    equalTo(s1, s2) {
        return s1 === s2;
    },
    notEqualTo(s1, s2) {
        return !filters.equalTo(s1, s2);
    },
};

const methods = {
    // Validate methods will return 'true' only when _s is true for each filter. Warn is raised when _filters contains
    // undefined filters.
    isValid(_s, _filters) {
        if (!_filters) return true;
        for (let i = 0; i < _filters.length; i += 1) {
            const filter = _filters[i];
            let filterName = filter;
            let params = null;
            if (typeof filter === 'object') {
                filterName = filter.name;
                params = filter.params;
            }
            if (!(filterName in filters)) {
                console.warn(`Filter ${filterName} doesn't exists.`);
            } else if (['equalTo', 'notEqualTo'].includes(filterName)) {
                // Special case, don't move this condition to upper 'else if'
                // equalTo and notEqualTo are not intended to have access to 'this' (component), so component data
                // property value is recovered here.
                if (params && !filters[filterName](_s, this.form[params.field].value)) return false;
            } else if (params && !filters[filterName](_s, params)) {
                return false;
            } else if (!params && !filters[filterName](_s)) {
                return false;
            }
        }
        return true;
    },
    isInvalid(_s, _filters) {
        if (!_filters) return false;
        for (let i = 0; i < _filters.length; i += 1) {
            const filter = _filters[i];
            let filterName = filter;
            let params = null;
            if (typeof filter === 'object') {
                filterName = filter.name;
                params = filter.params;
            }
            if (!(filterName in filters)) {
                console.warn(`Filter ${filterName} doesn't exists.`);
            } else if (['equalTo', 'notEqualTo'].includes(filterName)) {
                // Special case, don't move this condition to upper 'else if'
                // equalTo and notEqualTo are not intended to have access to 'this' (component), so component data
                // property value is recovered here.
                if (params && !filters[filterName](_s, this.form[params.field].value)) return false;
            } else if (params && filters[filterName](_s, params)) {
                return true;
            } else if (!params && filters[filterName](_s)) {
                return true;
            }
        }
        return false;
    },
    validateClasses(_o) {
        const value = _o.value;
        const classes = _o.classes;
        const validations = _o.validations;
        Object.keys(validations).forEach((key) => {
            if (key === 'is-valid') classes[key] = this.isValid(value, validations[key]);
            else if (key === 'is-invalid') classes[key] = this.isInvalid(value, validations[key]);
        });
        return classes;
    },
};

export default {
    methods,
    filters,
};
